<!-- Mission 2 | 2026-05-21 14:09:35 | 1051s | Path B -->

# Architecture Decision Record (ADR-001): Tech Stack Revisions Post-Validation

**From:** Architect Agent
**To:** Researcher (ack), Builder (heads-up), Legal (blockers), PM (UX impacts)
**Date:** 2026-05-21
**Re:** Incorporating Researcher's validation into Ctrip-Guides MVP architecture
**Status:** ACCEPTED — supersedes provisional stack from timed-out spec
**Project codename:** `ctrip_guides`

---

## 0. Acknowledgement

Researcher's report is comprehensive and addresses exactly the right risk surface. I'm adopting **4 of 5** recommendations wholesale and accepting **1 with a caveat**. Detailed below. Three items are escalated as **hard blockers** that must resolve before Builder can start sprint 1.

---

## 1. Revised Tech Stack — Locked Decisions

| Layer | Previous (provisional) | **New decision** | Rationale |
|---|---|---|---|
| Foreign-card acquiring | Stripe | **Airwallex (primary)** + Alipay Tour Pass + WeChat Pay International (secondary) | Researcher §1 — Stripe blocked by entity constraints; Airwallex is purpose-built for this flow |
| Cloud / hosting | Aliyun (mainland) | **Aliyun (mainland)** — confirmed | Researcher §2 — confirmed best-in-class for foreign-founded startups |
| Machine translation | Tencent MT | **Tencent MT (primary) + Aliyun MT (fallback)** | Researcher §3 — GFW-native, sub-100ms, trivial cost |
| Maps | Amap | **Amap (in-China) + Mapbox (outside-China web)** with server-side geo-routing | Researcher §4 — hybrid required; GCJ-02 compliance is non-negotiable |
| Real-time chat | Custom WebSocket | **Tencent Cloud IM (TIM)** | Researcher §5 — saves ~3–6 months of GFW-resilience engineering; managed push + offline + moderation hooks are compliance wins |

### Stack Frontend / Backend (unchanged from provisional)
- **Web frontend:** Vite + React + MUI + Tailwind CSS (i18n via `react-i18next`)
- **Mobile:** PWA first; React Native deferred to post-MVP
- **Backend:** Node.js (NestJS) — TypeScript end-to-end
- **DB:** Aliyun RDS PostgreSQL 15 (mainland region: `cn-hangzhou`)
- **Cache / queue:** Aliyun Redis + RocketMQ
- **Object storage:** Aliyun OSS (Beijing region)
- **CDN:** Aliyun CDN (mainland) + Aliyun Global Accelerator for tourist pre-trip browsing

---

## 2. The Mainland Entity Question (HARDEST BLOCKER)

Researcher correctly identifies this as the root constraint. Every decision below cascades from it.

### Decision tree the Founder must resolve before sprint 1:

```
                    ┌─ Path A: Incorporate WFOE in China
                    │   • 3–6 months, ~$5–15k
                    │   • Unlocks: ICP 备案, Aliyun mainland hosting,
                    │     Airwallex CNY settlement, full Amap commercial tier
                    │   • Risk: timeline kills MVP
                    │
Mainland entity? ───┼─ Path B: HK entity only (no mainland presence)
                    │   • Faster (2–4 weeks)
                    │   • Forces: HK/SG hosting (200–500ms RTT to mainland users)
                    │   • Forces: Airwallex HK contract; CNY payout to guides
                    │     becomes cross-border remittance per transaction (FX cost)
                    │   • ICP filing NOT possible → must use HK/SG domain
                    │
                    └─ Path C: Local partner / VIE
                        • Requires Legal sign-off
                        • Out of scope for Architect — flag only
```

**Architect's recommendation:** **Path A (WFOE)** is the only path that yields a defensible, scalable platform. Path B is a stopgap suitable for the first 90 days of customer discovery, but every Path B day adds technical debt (HK-hosted services, cross-border payment fees, no ICP). Founder should green-light WFOE incorporation **in parallel** with MVP build on Path B infrastructure, so we can cut over once incorporation closes.

---

## 3. Updated System Architecture Diagram (textual)

```
┌──────────────────────────────────────────────────────────────────────┐
│                        TOURISTS (outside China)                       │
│   Pre-trip browsing → Mapbox-backed map, Stripe-NOT-USED checkout    │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
            Aliyun Global Accelerator (anycast edge)
                               │
┌──────────────────────────────▼───────────────────────────────────────┐
│           Edge Router (Nginx + Lua geo-detection)                     │
│  - X-User-Region: CN vs ROW                                           │
│  - Routes map tile requests to Amap (CN) or Mapbox (ROW)              │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────────────┐
│                    NestJS API Gateway (Aliyun ECS)                    │
│  /api/v1/auth   /api/v1/guides   /api/v1/bookings   /api/v1/payments │
└──┬─────────┬─────────┬───────────┬──────────────┬────────────────────┘
   │         │         │           │              │
   ▼         ▼         ▼           ▼              ▼
┌──────┐ ┌──────┐ ┌────────┐ ┌──────────┐ ┌───────────────┐
│ PG   │ │Redis │ │Tencent │ │Airwallex │ │ Amap Places   │
│RDS   │ │      │ │  IM    │ │  API     │ │ (geocoding)   │
│      │ │      │ │  +     │ │  +       │ │               │
│      │ │      │ │Tencent │ │Alipay/WX │ │               │
│      │ │      │ │  MT    │ │  Intl    │ │               │
└──────┘ └──────┘ └────────┘ └──────────┘ └───────────────┘
                               │
                               ▼
                    Guide Bank Accounts (CNY)
                    via Airwallex CNY payout
```

---

## 4. Specific Changes to Hand to Builder

### 4.1 Chat module — switch from WS-custom to Tencent IM SDK

```typescript
// services/chat/tencent-im.adapter.ts
import TencentImSDK from 'tim-js-sdk';

interface ChatAdapter {
  sendMessage(roomId: string, payload: TranslatedMessage): Promise<void>;
  subscribe(roomId: string, onMessage: (m: TranslatedMessage) => void): Unsub;
  uploadMedia(file: File): Promise<string>;
}

// SDKAppID + UserSig provisioned by backend at /api/v1/chat/credentials
// Backend signs UserSig with TencentIM private key (HMAC-SHA256, TTL 7d)
```

**Builder task:** Remove `src/services/ws/*` skeleton. Implement `TencentIMAdapter` instead. Estimated savings: 4–6 weeks.

### 4.2 Payment module — Airwallex integration

```typescript
// POST /api/v1/payments/intent
// Body: { bookingId, currency: 'USD'|'EUR'|'GBP'|..., amount }
// Returns: { clientSecret, paymentIntentId, hostedCheckoutUrl }

// Webhook: POST /webhooks/airwallex
// Events: payment_intent.succeeded, payment_intent.failed, payout.completed
//   → Update bookings.payment_status
//   → Trigger guide payout job (T+1 settlement)
```

Database additions:
```sql
CREATE TABLE payments (
  id              UUID PRIMARY KEY,
  booking_id      UUID REFERENCES bookings(id),
  provider        TEXT NOT NULL CHECK (provider IN ('airwallex','alipay_intl','wechat_intl')),
  provider_ref    TEXT NOT NULL,            -- Airwallex paymentIntentId
  currency        CHAR(3) NOT NULL,
  amount_minor    BIGINT NOT NULL,          -- in smallest unit (cents)
  amount_cny_minor BIGINT,                  -- locked at payment time
  fx_rate         NUMERIC(12,6),
  status          TEXT NOT NULL,            -- pending|authorized|captured|refunded|failed
  created_at      TIMESTAMPTZ DEFAULT now(),
  captured_at     TIMESTAMPTZ
);

CREATE TABLE payouts (
  id              UUID PRIMARY KEY,
  guide_id        UUID REFERENCES guides(id),
  payment_id      UUID REFERENCES payments(id),
  amount_cny_minor BIGINT NOT NULL,
  platform_fee_cny_minor BIGINT NOT NULL,
  airwallex_payout_ref TEXT,
  status          TEXT NOT NULL,            -- scheduled|sent|completed|failed
  scheduled_for   DATE NOT NULL,            -- T+1 from booking completion
  completed_at    TIMESTAMPTZ
);
```

### 4.3 Maps module — geo-routed loader

```typescript
// src/lib/maps/index.ts
export async function loadMap(container: HTMLElement, opts: MapOpts) {
  const region = await detectRegion();  // GET /api/v1/region → 'CN' | 'ROW'
  if (region === 'CN') {
    const { AmapAdapter } = await import('./amap.adapter');
    return new AmapAdapter().mount(container, opts);
  } else {
    const { MapboxAdapter } = await import('./mapbox.adapter');
    return new MapboxAdapter().mount(container, opts);
  }
}
```

**Compliance note for Builder:** All coordinates stored server-side are **WGS-84**. Conversion to GCJ-02 happens only at the Amap adapter boundary using `coordtransform` npm package. NEVER store GCJ-02 in the DB.

### 4.4 Translation module — Tencent MT primary

```typescript
// services/translation/tencent-mt.adapter.ts
async translate(text: string, from: Lang, to: Lang): Promise<string>

// Cache layer: Redis with key sha256(`${from}:${to}:${text}`), TTL 30d
// Estimated hit rate >70% for chat (repeated greetings, prices, locations)
```

---

## 5. Updated File List for Builder (delta from provisional spec)

**Remove:**
- `src/services/ws/server.ts`
- `src/services/ws/reconnect-manager.ts`
- `src/services/ws/message-replay.ts`

**Add:**
- `src/services/chat/tencent-im.adapter.ts`
- `src/services/chat/usersig.signer.ts`
- `src/services/payments/airwallex.adapter.ts`
- `src/services/payments/alipay-intl.adapter.ts`
- `src/services/payments/wechat-intl.adapter.ts`
- `src/services/translation/tencent-mt.adapter.ts`
- `src/services/translation/aliyun-mt.fallback.ts`
- `src/lib/maps/amap.adapter.ts`
- `src/lib/maps/mapbox.adapter.ts`
- `src/lib/region.ts`
- `src/middleware/region-detect.middleware.ts`

---

## 6. Open Items / Blockers (Owners Assigned)

| # | Item | Owner | Blocks |
|---|---|---|---|
| B1 | WFOE vs HK-only decision | Founder + Legal | Hosting region, ICP filing, Airwallex contract, all sprint 1 |
| B2 | ICP 证 (commercial) vs 备案 only for marketplace | Legal | Domain go-live date |
| B3 | Surveying & Mapping Law compliance review (Amap commercial usage tier) | Legal | Map feature launch |
| B4 | Airwallex KYB initiation (entity-dependent) | Founder | Payment integration sprint |
| B5 | Tencent IM SDKAppID provisioning (need entity for paid tier) | Architect | Chat sprint kickoff |
| B6 | Confirm tourist-side PWA is acceptable for App Store discoverability or whether a native shell is needed for stores | PM | Mobile strategy |

---

## 7. What Builder Can Start RIGHT NOW (entity-independent)

Even before the WFOE/HK decision lands, the following are safe to begin:

1. **Repo scaffold** — Vite + React + MUI + Tailwind monorepo (web + api)
2. **Domain modeling** — `guides`, `tourists`, `bookings`, `cities`, `certifications`, `reviews` tables (DDL ready in next handoff)
3. **i18n skeleton** — EN, ZH-CN, JA, KO message catalogs
4. **Guide-onboarding wizard UI** (no payment hookup yet)
5. **Search & matching algorithm v1** — see ADR-002 (forthcoming, will replace the original MVP spec section)
6. **CI/CD** — GitHub Actions targeting Aliyun Container Registry (will configure region after B1 resolves)

---

## 8. Anything UNCLEAR

- **Airwallex KYB on HK entity for mainland-paying guides:** Researcher flagged this as needs-verification. Architect concurs — request Founder ask Airwallex sales directly: *"Can a HK entity onboard, accept foreign cards, and pay out to mainland CNY accounts held by individual contractors (guides) without those guides being registered businesses?"* The "individual contractor payout" piece is the part that often breaks.
- **Tencent IM moderation hooks:** Need to confirm whether Tencent IM's built-in content moderation satisfies §47 of the Cybersecurity Law's keyword-filter requirement, or whether we need to layer Aliyun Green or Tencent CMS on top. Defer to Legal review (B2 follow-up).
- **PWA vs native shell:** Per the SYSTEM brief, "mobile-first design (tourists are traveling)". PWA works on iOS Safari but loses iOS push notifications. Recommend native shell (Capacitor over the same React codebase) as a fast-follow once MVP web is stable.

---

## Next Architect Deliverables (queued)

- **ADR-002:** Matching algorithm v1 (tourist intent → guide ranking) — pure logic, entity-independent, will produce next.
- **ADR-003:** Database DDL + ER diagram — entity-independent, will produce after ADR-002.
- **Full MVP Tech Spec rewrite** (replacing the timed-out one) — gated on B1 resolution, target 48h after Founder decides on entity path.

**Researcher: thank you. This unblocked 4 of 5 stack decisions cleanly. Recommending we keep this same validation pattern (Architect proposes → Researcher validates → ADR locks) for ADR-002 and ADR-003.**