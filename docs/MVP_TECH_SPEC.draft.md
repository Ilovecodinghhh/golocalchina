# Ctrip-Guides MVP Technical Specification
**Path B: Pure Information Matching Platform (信息技术服务)**

- **Author:** Architect
- **Date:** 2026-05-21
- **Status:** DRAFT v0.1 — pending Legal stamp
- **Scope:** MVP launch, 4 cities (Beijing, Shanghai, Xi'an, Chengdu), ~50 guides

---

## 0. Legal Posture (NON-NEGOTIABLE)

> Every technical decision below is constrained by these rules. Builder MUST NOT introduce features that violate them without re-architecture review.

| # | Rule | Engineering Implication |
|---|------|------------------------|
| L1 | We are an **information matching service** (信息技术服务), **NOT** a travel agency (旅行社). | No "tour" / "package" / "itinerary sold by us" anywhere in UI copy or DB schema. |
| L2 | Guides are **independent contractors**. We do not employ them. | Contracts table flags `relationship = 'independent_contractor'`. No payroll, no scheduling enforcement. |
| L3 | We do **NOT** set prices. Guides set their own rates. | `service_listings.price_cny` is guide-editable. Platform has no `recommended_price` field exposed to guide. |
| L4 | We do **NOT** bundle transport, lodging, tickets. | No `transport_*`, `hotel_*`, `ticket_*` tables. Cross-sell links are external referrals only, clearly labeled. |
| L5 | We do **NOT** hold funds in escrow as a tour operator. Payments are facilitated, not collected as agent. | Payment flow uses payment provider's "marketplace/split" mode → guide is merchant of record where possible. |
| L6 | Disputes between tourist ↔ guide are between **them**. Platform mediates good-faith only. | ToS makes this explicit. Refund engine has limited scope. |
| L7 | All UI copy must read **"connect with"**, **"book a guide's time"**, **"information service fee"** — NEVER "tour", "package", "我们的导游" (our guides). | i18n strings reviewed by Legal pre-launch. |
| L8 | ICP filing (备案) required for domestic hosting. Use Aliyun/Tencent Cloud Shanghai region. | DNS + hosting plan locked to filed domain. |

---

## 1. Architecture Overview

### 1.1 Implementation Approach
Lean monolith → modular monolith. We optimize for **2 engineers, 8-week MVP**, not microservices.

- **Backend:** Python 3.11 + FastAPI (async, OpenAPI auto-gen, type safety)
- **DB:** PostgreSQL 15 (Aliyun RDS, Shanghai)
- **Cache/Queue:** Redis 7 (Aliyun)
- **Frontend (tourist):** Vite + React + MUI + Tailwind, PWA-first (foreign tourists arrive without app)
- **Frontend (guide):** WeChat Mini Program (guides are domestic, already use WeChat)
- **Search/match:** Postgres + `pg_trgm` + `tsvector` (no Elasticsearch for MVP)
- **Hosting:** Aliyun ECS Shanghai (ICP filed) + Aliyun CDN
- **Object storage:** Aliyun OSS (guide photos, certs)
- **Observability:** Aliyun ARMS + structured JSON logs

### 1.2 Why this stack survives China constraints
- Domestic hosting → no GFW latency for guides (who are in China)
- Tourist PWA served via CDN with international acceleration (Aliyun DCDN)
- WeChat Mini Program = zero-install for guides
- FastAPI's OpenAPI → frontend types auto-generated

---

## 2. Service Boundaries (modular monolith)

```
apps/api/
├── modules/
│   ├── identity/       # auth, KYC for guides
│   ├── catalog/        # guide profiles, service listings
│   ├── matching/       # search + rank
│   ├── booking/        # time-slot reservation
│   ├── messaging/      # tourist ↔ guide chat
│   ├── payments/       # provider integrations (split payments)
│   ├── reviews/        # post-trip ratings
│   ├── compliance/     # audit log, content moderation hooks
│   └── i18n/           # currency, locale, timezone
```

Each module exposes a Python interface; cross-module calls go through interfaces, not direct DB. This lets us extract services later without rewrite.

---

## 3. Data Model (PostgreSQL)

### 3.1 Core tables

```sql
-- 3.1.1 Users (both sides)
CREATE TABLE users (
  id              BIGSERIAL PRIMARY KEY,
  user_type       TEXT NOT NULL CHECK (user_type IN ('tourist','guide','admin')),
  email           TEXT UNIQUE,
  phone_e164      TEXT UNIQUE,
  wechat_openid   TEXT UNIQUE,                 -- guides only
  locale          TEXT NOT NULL DEFAULT 'en',
  preferred_ccy   TEXT NOT NULL DEFAULT 'USD',
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  status          TEXT NOT NULL DEFAULT 'active'
);

-- 3.1.2 Guide profiles (one-to-one with users where user_type='guide')
CREATE TABLE guide_profiles (
  user_id            BIGINT PRIMARY KEY REFERENCES users(id),
  display_name       TEXT NOT NULL,
  city               TEXT NOT NULL CHECK (city IN ('beijing','shanghai','xian','chengdu')),
  bio_zh             TEXT,
  bio_en             TEXT,
  languages          TEXT[] NOT NULL,          -- ISO codes: ['en','zh','ja']
  avatar_url         TEXT,
  cert_number        TEXT NOT NULL,            -- 导游证号 (L2: independent professional)
  cert_verified_at   TIMESTAMPTZ,
  cert_image_url     TEXT,
  relationship       TEXT NOT NULL DEFAULT 'independent_contractor',  -- L2
  kyc_status         TEXT NOT NULL DEFAULT 'pending',
  rating_avg         NUMERIC(3,2),
  rating_count       INT NOT NULL DEFAULT 0
);

-- 3.1.3 Service listings (NOT "tours" — L1)
CREATE TABLE service_listings (
  id              BIGSERIAL PRIMARY KEY,
  guide_id        BIGINT NOT NULL REFERENCES guide_profiles(user_id),
  title_en        TEXT NOT NULL,
  title_zh        TEXT NOT NULL,
  description_en  TEXT,
  description_zh  TEXT,
  city            TEXT NOT NULL,
  duration_hours  NUMERIC(4,1) NOT NULL,
  price_cny       NUMERIC(10,2) NOT NULL,       -- L3: guide-set
  price_self_set  BOOLEAN NOT NULL DEFAULT TRUE,-- L3 enforcement flag
  themes          TEXT[],                       -- ['history','food','family']
  meeting_point   TEXT,                         -- NOT pickup; guide doesn't provide transport (L4)
  active          BOOLEAN NOT NULL DEFAULT TRUE,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 3.1.4 Availability (guide's own calendar; we don't schedule them — L2)
CREATE TABLE guide_availability (
  id            BIGSERIAL PRIMARY KEY,
  guide_id      BIGINT NOT NULL REFERENCES guide_profiles(user_id),
  start_ts      TIMESTAMPTZ NOT NULL,           -- stored UTC; rendered in Asia/Shanghai
  end_ts        TIMESTAMPTZ NOT NULL,
  status        TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open','held','booked','blocked'))
);
CREATE INDEX idx_availability_guide_time ON guide_availability(guide_id, start_ts);

-- 3.1.5 Bookings
CREATE TABLE bookings (
  id                BIGSERIAL PRIMARY KEY,
  tourist_id        BIGINT NOT NULL REFERENCES users(id),
  guide_id          BIGINT NOT NULL REFERENCES guide_profiles(user_id),
  listing_id        BIGINT NOT NULL REFERENCES service_listings(id),
  start_ts          TIMESTAMPTZ NOT NULL,
  end_ts            TIMESTAMPTZ NOT NULL,
  party_size        INT NOT NULL,
  price_cny         NUMERIC(10,2) NOT NULL,     -- snapshot of guide's rate at booking time
  service_fee_cny   NUMERIC(10,2) NOT NULL,     -- L7: "information service fee", NOT commission of a tour
  currency_paid     TEXT NOT NULL,              -- e.g. 'USD'
  fx_rate           NUMERIC(12,6) NOT NULL,
  amount_paid       NUMERIC(12,2) NOT NULL,
  status            TEXT NOT NULL DEFAULT 'pending'
                    CHECK (status IN ('pending','confirmed','completed','cancelled','disputed')),
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 3.1.6 Payments (split mode — L5)
CREATE TABLE payments (
  id              BIGSERIAL PRIMARY KEY,
  booking_id      BIGINT NOT NULL REFERENCES bookings(id),
  provider        TEXT NOT NULL,                -- 'stripe_cn'|'alipay_global'|'unionpay'
  provider_ref    TEXT NOT NULL,
  gross_amount    NUMERIC(12,2) NOT NULL,
  guide_payout    NUMERIC(12,2) NOT NULL,       -- goes directly to guide
  platform_fee    NUMERIC(12,2) NOT NULL,       -- our information-service fee
  ccy             TEXT NOT NULL,
  status          TEXT NOT NULL,
  raw_payload     JSONB
);

-- 3.1.7 Messages (in-app chat)
CREATE TABLE messages (
  id          BIGSERIAL PRIMARY KEY,
  booking_id  BIGINT REFERENCES bookings(id),
  sender_id   BIGINT NOT NULL REFERENCES users(id),
  body        TEXT NOT NULL,
  lang_detected TEXT,
  translated_body TEXT,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 3.1.8 Reviews
CREATE TABLE reviews (
  id          BIGSERIAL PRIMARY KEY,
  booking_id  BIGINT UNIQUE NOT NULL REFERENCES bookings(id),
  rating      SMALLINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
  body        TEXT,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 3.1.9 Audit (L8 compliance)
CREATE TABLE audit_log (
  id          BIGSERIAL PRIMARY KEY,
  actor_id    BIGINT,
  action      TEXT NOT NULL,
  entity      TEXT NOT NULL,
  entity_id   BIGINT,
  payload     JSONB,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### 3.2 Notable schema decisions tied to legal posture
- **No `tours` table.** Only `service_listings` (L1).
- **No `transport`, `hotel`, `ticket` tables.** (L4)
- **`relationship` column on guide_profiles** locked to `independent_contractor` (L2).
- **`service_fee_cny` is "information service fee"**, not "commission" (L7).
- **`price_self_set` boolean** acts as a runtime assertion for L3.

---

## 4. API Contracts (FastAPI, OpenAPI auto-gen)

Base: `https://api.ctrip-guides.cn/v1`  (ICP-filed domain — L8)

### 4.1 Tourist endpoints (foreign-facing)

| Method | Path | Purpose |
|--------|------|---------|
| POST   | `/auth/email/start` | Email magic-link (no SMS for foreign #s) |
| POST   | `/auth/email/verify` | Exchange token → JWT |
| GET    | `/guides/search` | Search by `city`, `date`, `language`, `theme` |
| GET    | `/guides/{id}` | Public profile |
| GET    | `/listings/{id}` | Listing detail |
| GET    | `/listings/{id}/availability?from=&to=` | Open slots |
| POST   | `/bookings` | Create booking (status=pending) |
| POST   | `/bookings/{id}/pay` | Initiate payment, returns provider redirect |
| GET    | `/bookings/{id}` | Booking detail |
| POST   | `/bookings/{id}/cancel` | Cancel (refund per policy) |
| GET    | `/messages?booking_id=` | List messages |
| POST   | `/messages` | Send message |
| POST   | `/reviews` | Post-trip review |

### 4.2 Guide endpoints (WeChat Mini Program)

| Method | Path | Purpose |
|--------|------|---------|
| POST   | `/guide/auth/wechat` | WeChat login |
| POST   | `/guide/kyc` | Upload 导游证 |
| GET/PUT| `/guide/profile` | Self-edit profile |
| GET/POST/PUT/DELETE | `/guide/listings` | CRUD listings (price = guide's choice, L3) |
| GET/POST/DELETE | `/guide/availability` | CRUD time slots |
| GET    | `/guide/bookings` | Incoming bookings |
| POST   | `/guide/bookings/{id}/accept` | Accept |
| POST   | `/guide/bookings/{id}/decline` | Decline |
| GET    | `/guide/payouts` | Payout history |

### 4.3 Request/response example

```http
POST /v1/guides/search
{
  "city": "xian",
  "date": "2026-06-12",
  "language": "en",
  "themes": ["history"],
  "party_size": 2
}

200 OK
{
  "results": [
    {
      "guide_id": 17,
      "display_name": "Wei L.",
      "city": "xian",
      "languages": ["en","zh"],
      "rating_avg": 4.86,
      "rating_count": 42,
      "listings": [
        {
          "id": 103,
          "title_en": "Terracotta Warriors with a historian",
          "duration_hours": 6.0,
          "price_cny": 1200.00,
          "price_self_set": true,
          "next_available": "2026-06-12T09:00:00+08:00"
        }
      ]
    }
  ],
  "match_score_explanation": "ranked by language match, rating, and availability proximity"
}
```

---

## 5. Matching Algorithm (MVP — simple, explainable)

For 50 guides we do **not** need ML. We do **need** transparency for the founders.

### 5.1 Inputs
- Tourist filters: `city` (hard), `date` (hard), `language` (hard), `themes` (soft), `party_size` (hard)
- Guide attributes: `languages`, `themes`, `rating_avg`, `rating_count`, availability

### 5.2 Score (range 0–1)
```
score = 0.30 * language_match        # exact match = 1, else 0
      + 0.25 * theme_overlap         # |intersect| / |requested|
      + 0.20 * rating_norm           # rating_avg / 5
      + 0.15 * availability_proximity# 1 - (days_to_next_slot / 30), clipped 0
      + 0.10 * review_volume_log     # log1p(rating_count) / log1p(100), capped 1
```
- Hard filters applied first (city, date open, language available, party_size ≤ max).
- Tie-break: rating_count desc, then random with stable seed (fair rotation for new guides).

### 5.3 No price-based ranking
**Deliberate (L3):** we do not rank by price, nor expose "recommended price" to guides. Sorting by price is a tourist-side UI option only, not a platform recommendation.

---

## 6. User Flows

### 6.1 Tourist happy path
1. Lands on `m.ctrip-guides.cn` (PWA, English default by `Accept-Language`)
2. Picks city + dates + language → search results
3. Opens guide profile → reads bio, reviews, sees listings
4. Selects listing + time slot → "Request to book"
5. Pays via Stripe (foreign card → CNY split: guide payout + platform fee)
6. Guide accepts within 24h (auto-decline + refund if not)
7. In-app chat opens; meeting point shared
8. After trip: review prompt

### 6.2 Guide onboarding
1. Scans QR → opens WeChat Mini Program
2. WeChat login → KYC: upload 导游证 + ID
3. Admin reviews (manual for first 50)
4. Guide creates first listing (price self-set; UI shows L3 reminder)
5. Adds availability
6. Goes live

---

## 7. i18n / FX / Timezone

- **Locales:** `en` (primary), `zh`, `ja`, `ko`, `es`. Fallback chain `xx → en`.
- **Currencies displayed:** USD, EUR, GBP, JPY, KRW, CNY. Stored in CNY; FX snapshot frozen at booking (`bookings.fx_rate`).
- **FX source:** daily pull from `exchangerate.host` cached in Redis; manual override flag for ops.
- **Timezones:** all DB UTC; UI renders in `Asia/Shanghai` for trip times, tourist's locale for everything else.

---

## 8. Payments — Path B compliant flow (L5)

```
Tourist (foreign card)
  → Stripe (international acquiring)
  → split payout:
       ├── 85% → Guide's account (merchant of record where feasible)
       └── 15% → Platform "information service fee"
```

- Stripe Connect (or Adyen MarketPay) handles the split → platform never sits on guide funds beyond settlement window.
- Alipay Global / WeChat Pay HK as alternates (🚩 confirmed scope w/ Researcher; commitment pending Legal).
- Refund policy: tourist cancels >72h before = full refund minus FX cost; <72h = guide-defined policy (L6).

---

## 9. Security & Compliance

- HTTPS everywhere, HSTS, TLS 1.3
- JWT (15-min access + 7-day refresh), rotating signing keys via KMS
- Rate limiting at gateway (per-IP + per-user)
- PII at rest: column-level encryption for `phone_e164`, `cert_number`, `cert_image_url`
- **PIPL (个人信息保护法):** data of Chinese users stored in Shanghai; export of foreigners' data requires consent dialog
- **ICP filing** (L8) prerequisite to production launch
- Content moderation: profanity + L1/L4/L7 forbidden-term detector on listing creation (e.g., blocks "tour package", "we provide transport")
- Audit log on every state-change action (3.1.9)

---

## 10. Observability

- Structured JSON logs → Aliyun SLS
- Metrics: bookings/day, search→booking funnel, guide response time, payment success
- Error tracking: Sentry (self-hosted) or Aliyun ARMS
- Daily backup of RDS + OSS versioning

---

## 11. Deployment Topology

```
Aliyun Shanghai region
├── ECS x2 (api, behind SLB)
├── RDS PostgreSQL (multi-AZ)
├── Redis (cluster mode)
├── OSS (private bucket + signed URLs)
├── DCDN (tourist PWA, global acceleration)
└── Function Compute (FX cron, payout reconciliation cron)
```

CI/CD: GitHub Actions → Aliyun Container Registry → ECS rolling deploy.

---

## 12. MVP Scope Cuts (deliberately out)

- ❌ Native iOS/Android apps (PWA + Mini Program suffice)
- ❌ AI itinerary generation (L1 risk — would look like tour planning)
- ❌ Group/multi-guide bookings (post-MVP)
- ❌ Tipping flow (post-MVP)
- ❌ Loyalty program
- ❌ Elasticsearch / vector search (Postgres FTS is enough at 50 guides)
- ❌ Microservices

---

## 13. Builder Task Breakdown (sprint-sized)

| # | Task | Est. | Depends |
|---|------|------|---------|
| T1 | Repo skeleton, FastAPI, Postgres, Docker compose | 2d | — |
| T2 | DB migrations for §3 schema | 2d | T1 |
| T3 | Auth: tourist email magic-link + guide WeChat | 4d | T2 |
| T4 | Guide profile + KYC upload (admin manual approve) | 3d | T3 |
| T5 | Listings CRUD with L1/L3/L4 copy guards | 3d | T4 |
| T6 | Availability + search/match (§5) | 4d | T5 |
| T7 | Booking lifecycle (create/accept/cancel) | 4d | T6 |
| T8 | Stripe Connect split payments | 5d | T7 |
| T9 | Messaging + post-trip review | 3d | T7 |
| T10 | Tourist PWA (React+MUI+Tailwind) | 7d | T6 |
| T11 | Guide WeChat Mini Program | 6d | T5 |
| T12 | Admin console (manual KYC, dispute view) | 3d | T7 |
| T13 | i18n + FX + Asia/Shanghai TZ rendering | 3d | T10 |
| T14 | Audit log + forbidden-term moderator | 2d | T5 |
| T15 | ICP filing prep (legal+ops, parallel) | (legal) | — |
| T16 | Load test + security review | 3d | T8,T9,T10 |

**Critical path:** T1→T2→T3→T5→T6→T7→T8→T16 ≈ 27 dev-days. With 2 engineers + parallelism: ~7-8 weeks ✅

---

## 14. Open Questions (need Legal / Founder rulings)

1. 🚩 **Stripe Connect "merchant of record"** — does guide-as-MoR work given they're individuals (not 个体工商户)? May force us to MoR with explicit "information service" invoice. → Legal.
2. 🚩 **Cert verification source** — is there an official API for 导游证 lookup, or manual photo review only? → Researcher follow-up.
3. 🚩 **Tax handling** — VAT/fapiao on the 15% platform fee. Domestic CNY invoicing requires tax registration. → Legal+Finance.
4. 🚩 **Cross-border data** — foreigners' personal data leaving China for analytics needs PIPL Article 38 path. → Legal.
5. **Dispute policy concrete text** — Legal must draft, we wire UI to it. (L6)

---

## 15. Handoff to Builder

Builder, when you pick this up:
- Start with **T1 + T2** as a single PR; that unblocks everything.
- The forbidden-term list in T14 is a **shared module** used by T5, T9, T11 — write it once.
- Every PR touching listings, bookings, or copy must include the line *"Legal posture check: L1–L7 reviewed"* in the description.
- If a feature requirement conflicts with §0, **stop and escalate** to Architect — do not work around it.

— Architect
