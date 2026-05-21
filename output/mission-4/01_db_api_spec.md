# Ctrip-Guides — DDL + API Specification (Builder Handoff)

**Path:** B (no tour/package/itinerary tables) · **Stack:** FastAPI + PostgreSQL 15 + SQLAlchemy/Alembic + Redis + JWT · **PSP:** Airwallex

---

## 1. Complete DDL (PostgreSQL 15)

```sql
-- =========================================================================
-- EXTENSIONS
-- =========================================================================
CREATE EXTENSION IF NOT EXISTS "pgcrypto";   -- gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS "citext";     -- case-insensitive email
CREATE EXTENSION IF NOT EXISTS "postgis";    -- geo search for guide service areas
CREATE EXTENSION IF NOT EXISTS "pg_trgm";    -- fuzzy text search

-- =========================================================================
-- ENUMS
-- =========================================================================
CREATE TYPE user_role         AS ENUM ('tourist', 'guide', 'admin');
CREATE TYPE user_status       AS ENUM ('pending', 'active', 'suspended', 'deleted');
CREATE TYPE kyc_status        AS ENUM ('unsubmitted', 'pending', 'approved', 'rejected');
CREATE TYPE listing_status    AS ENUM ('draft', 'published', 'paused', 'archived');
CREATE TYPE request_status    AS ENUM (
    'pending',        -- tourist submitted, awaiting guide
    'accepted',       -- guide accepted, awaiting payment
    'paid',           -- escrowed at PSP
    'confirmed',      -- both parties locked
    'in_progress',
    'completed',
    'cancelled_by_tourist',
    'cancelled_by_guide',
    'refunded',
    'disputed'
);
CREATE TYPE payment_status    AS ENUM ('initiated', 'authorized', 'captured', 'failed', 'refunded', 'partially_refunded');
CREATE TYPE payout_status     AS ENUM ('scheduled', 'processing', 'paid', 'failed', 'on_hold');
CREATE TYPE review_direction  AS ENUM ('tourist_to_guide', 'guide_to_tourist');
CREATE TYPE message_kind      AS ENUM ('text', 'image', 'system', 'location');
CREATE TYPE consent_scope     AS ENUM ('pipl_personal_data', 'pipl_cross_border', 'marketing', 'cookies');
CREATE TYPE audit_actor       AS ENUM ('user', 'system', 'admin', 'webhook');

-- =========================================================================
-- USERS (auth root)
-- =========================================================================
CREATE TABLE users (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email               CITEXT UNIQUE,
    phone_e164          VARCHAR(20) UNIQUE,
    password_hash       VARCHAR(255) NOT NULL,
    role                user_role    NOT NULL,
    status              user_status  NOT NULL DEFAULT 'pending',
    locale              VARCHAR(10)  NOT NULL DEFAULT 'en-US',
    timezone            VARCHAR(64)  NOT NULL DEFAULT 'Asia/Shanghai',
    email_verified_at   TIMESTAMPTZ,
    phone_verified_at   TIMESTAMPTZ,
    last_login_at       TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT users_contact_chk CHECK (email IS NOT NULL OR phone_e164 IS NOT NULL)
);
CREATE INDEX idx_users_role_status ON users(role, status);
CREATE INDEX idx_users_created_at  ON users(created_at DESC);

-- =========================================================================
-- TOURIST PROFILES
-- =========================================================================
CREATE TABLE tourist_profiles (
    user_id             UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    display_name        VARCHAR(80)  NOT NULL,
    nationality         CHAR(2),                       -- ISO 3166-1 alpha-2
    preferred_currency  CHAR(3) NOT NULL DEFAULT 'USD',-- ISO 4217
    preferred_languages VARCHAR(10)[] NOT NULL DEFAULT '{}',
    passport_country    CHAR(2),
    avatar_url          TEXT,
    bio                 TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =========================================================================
-- GUIDE PROFILES (导游证 verification)
-- =========================================================================
CREATE TABLE guide_profiles (
    user_id              UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    legal_name           VARCHAR(120) NOT NULL,
    display_name         VARCHAR(80)  NOT NULL,
    -- 导游证 (Tour Guide Certificate) fields
    guide_license_no     VARCHAR(40)  UNIQUE NOT NULL,   -- 导游证号
    guide_license_issuer VARCHAR(120) NOT NULL,          -- 发证机关 (省/市文旅局)
    guide_license_issued_on  DATE      NOT NULL,
    guide_license_expires_on DATE      NOT NULL,
    guide_license_scan_url   TEXT      NOT NULL,         -- private OSS URL
    id_card_last4        CHAR(4)      NOT NULL,          -- 身份证后四位
    kyc_status           kyc_status   NOT NULL DEFAULT 'unsubmitted',
    kyc_reviewed_by      UUID         REFERENCES users(id),
    kyc_reviewed_at      TIMESTAMPTZ,
    kyc_rejection_reason TEXT,
    -- service profile
    languages            VARCHAR(10)[] NOT NULL DEFAULT '{}',  -- BCP-47 codes
    service_cities       TEXT[]        NOT NULL DEFAULT '{}',  -- e.g. {"Beijing","Xi'an"}
    service_area_geom    geography(MULTIPOLYGON, 4326),        -- optional geo fence
    years_experience     SMALLINT     NOT NULL DEFAULT 0,
    specialties          TEXT[]       NOT NULL DEFAULT '{}',   -- {"history","food","hiking"}
    bio                  TEXT,
    avatar_url           TEXT,
    intro_video_url      TEXT,
    rating_avg           NUMERIC(3,2) NOT NULL DEFAULT 0.00,   -- denormalized
    rating_count         INTEGER      NOT NULL DEFAULT 0,
    response_rate_pct    SMALLINT     NOT NULL DEFAULT 0,
    response_time_minutes INTEGER     NOT NULL DEFAULT 0,
    created_at           TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at           TIMESTAMPTZ  NOT NULL DEFAULT now(),
    CONSTRAINT guide_license_valid_dates CHECK (guide_license_expires_on > guide_license_issued_on)
);
CREATE INDEX idx_guide_kyc_status      ON guide_profiles(kyc_status);
CREATE INDEX idx_guide_cities          ON guide_profiles USING GIN (service_cities);
CREATE INDEX idx_guide_languages       ON guide_profiles USING GIN (languages);
CREATE INDEX idx_guide_specialties     ON guide_profiles USING GIN (specialties);
CREATE INDEX idx_guide_rating          ON guide_profiles(rating_avg DESC, rating_count DESC);
CREATE INDEX idx_guide_service_area    ON guide_profiles USING GIST (service_area_geom);

-- =========================================================================
-- GUIDE LISTINGS (guide-authored, guide-owned offerings)
-- NOTE: NOT tours/packages/itineraries. A listing is a guide's service offer.
-- =========================================================================
CREATE TABLE guide_listings (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guide_user_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title               VARCHAR(160) NOT NULL,
    summary             VARCHAR(500) NOT NULL,
    description_md      TEXT NOT NULL,
    city                VARCHAR(80) NOT NULL,
    meeting_point_text  VARCHAR(255),
    meeting_point_geo   geography(POINT, 4326),
    languages           VARCHAR(10)[] NOT NULL DEFAULT '{}',
    -- Guide-set pricing (no platform price control)
    price_amount        NUMERIC(12,2) NOT NULL CHECK (price_amount >= 0),
    price_currency      CHAR(3)       NOT NULL DEFAULT 'CNY',
    price_unit          VARCHAR(20)   NOT NULL DEFAULT 'per_half_day', -- per_hour | per_half_day | per_day
    min_duration_hours  NUMERIC(4,1)  NOT NULL DEFAULT 4.0,
    max_group_size      SMALLINT      NOT NULL DEFAULT 8,
    cover_image_url     TEXT,
    gallery_urls        TEXT[]        NOT NULL DEFAULT '{}',
    tags                TEXT[]        NOT NULL DEFAULT '{}',
    status              listing_status NOT NULL DEFAULT 'draft',
    published_at        TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_listings_guide        ON guide_listings(guide_user_id);
CREATE INDEX idx_listings_status_city  ON guide_listings(status, city);
CREATE INDEX idx_listings_languages    ON guide_listings USING GIN (languages);
CREATE INDEX idx_listings_tags         ON guide_listings USING GIN (tags);
CREATE INDEX idx_listings_title_trgm   ON guide_listings USING GIN (title gin_trgm_ops);
CREATE INDEX idx_listings_geo          ON guide_listings USING GIST (meeting_point_geo);

-- =========================================================================
-- AVAILABILITY SLOTS (per-guide working windows)
-- =========================================================================
CREATE TABLE availability_slots (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guide_user_id   UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    starts_at       TIMESTAMPTZ NOT NULL,
    ends_at         TIMESTAMPTZ NOT NULL,
    is_blocked      BOOLEAN     NOT NULL DEFAULT FALSE, -- TRUE = explicitly unavailable
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT slot_range_chk CHECK (ends_at > starts_at),
    CONSTRAINT slot_no_overlap EXCLUDE USING gist (
        guide_user_id WITH =,
        tstzrange(starts_at, ends_at, '[)') WITH &&
    )
);
CREATE INDEX idx_slots_guide_range ON availability_slots(guide_user_id, starts_at, ends_at);

-- =========================================================================
-- SERVICE REQUESTS (tourist → guide connection)
-- =========================================================================
CREATE TABLE service_requests (
    id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tourist_user_id       UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    guide_user_id         UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    listing_id            UUID REFERENCES guide_listings(id) ON DELETE SET NULL,
    service_date          DATE NOT NULL,
    starts_at             TIMESTAMPTZ NOT NULL,
    ends_at               TIMESTAMPTZ NOT NULL,
    party_size            SMALLINT NOT NULL CHECK (party_size BETWEEN 1 AND 30),
    language              VARCHAR(10) NOT NULL,
    tourist_notes         TEXT,
    -- Pricing snapshot at request time (guide-set)
    quoted_amount         NUMERIC(12,2) NOT NULL,
    quoted_currency       CHAR(3)       NOT NULL,
    platform_fee_pct      NUMERIC(5,2)  NOT NULL DEFAULT 12.00,   -- 信息服务费
    platform_fee_amount   NUMERIC(12,2) NOT NULL,
    guide_payout_amount   NUMERIC(12,2) NOT NULL,                 -- quoted - fee
    status                request_status NOT NULL DEFAULT 'pending',
    accepted_at           TIMESTAMPTZ,
    cancelled_at          TIMESTAMPTZ,
    cancellation_reason   TEXT,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at            TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT sr_time_chk CHECK (ends_at > starts_at),
    CONSTRAINT sr_distinct_parties CHECK (tourist_user_id <> guide_user_id)
);
CREATE INDEX idx_sr_tourist        ON service_requests(tourist_user_id, status, created_at DESC);
CREATE INDEX idx_sr_guide          ON service_requests(guide_user_id, status, created_at DESC);
CREATE INDEX idx_sr_status_date    ON service_requests(status, service_date);

-- =========================================================================
-- CONNECTIONS (long-lived guide↔tourist channel; 1 per accepted request)
-- =========================================================================
CREATE TABLE connections (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_request_id  UUID NOT NULL UNIQUE REFERENCES service_requests(id) ON DELETE CASCADE,
    tourist_user_id     UUID NOT NULL REFERENCES users(id),
    guide_user_id       UUID NOT NULL REFERENCES users(id),
    opened_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    closed_at           TIMESTAMPTZ,
    last_message_at     TIMESTAMPTZ
);
CREATE INDEX idx_connections_tourist ON connections(tourist_user_id, last_message_at DESC);
CREATE INDEX idx_connections_guide   ON connections(guide_user_id,   last_message_at DESC);

-- =========================================================================
-- PAYMENTS (Airwallex; platform never holds funds)
-- =========================================================================
CREATE TABLE payments (
    id                       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_request_id       UUID NOT NULL REFERENCES service_requests(id) ON DELETE RESTRICT,
    payer_user_id            UUID NOT NULL REFERENCES users(id),
    -- Airwallex refs
    airwallex_intent_id      VARCHAR(64)  UNIQUE NOT NULL,   -- PaymentIntent id
    airwallex_customer_id    VARCHAR(64),
    airwallex_charge_id      VARCHAR(64),
    client_secret_redacted   VARCHAR(32),                    -- last 8 chars only
    -- Amounts
    amount                   NUMERIC(12,2) NOT NULL,
    currency                 CHAR(3)       NOT NULL,
    settlement_currency      CHAR(3)       NOT NULL DEFAULT 'CNY',
    fx_rate                  NUMERIC(14,8),
    platform_fee_amount      NUMERIC(12,2) NOT NULL,
    psp_fee_amount           NUMERIC(12,2) NOT NULL DEFAULT 0,
    net_to_guide_amount      NUMERIC(12,2) NOT NULL,
    status                   payment_status NOT NULL DEFAULT 'initiated',
    failure_code             VARCHAR(64),
    failure_message          TEXT,
    captured_at              TIMESTAMPTZ,
    refunded_at              TIMESTAMPTZ,
    raw_webhook_jsonb        JSONB,
    created_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at               TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_payments_sr     ON payments(service_request_id);
CREATE INDEX idx_payments_status ON payments(status, created_at DESC);

-- =========================================================================
-- PAYOUTS (CNY out to guides via Airwallex Payouts)
-- =========================================================================
CREATE TABLE payouts (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guide_user_id           UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    payment_id              UUID NOT NULL REFERENCES payments(id) ON DELETE RESTRICT,
    amount_cny              NUMERIC(12,2) NOT NULL,
    -- Airwallex Payout/Beneficiary refs
    airwallex_payout_id     VARCHAR(64) UNIQUE,
    airwallex_beneficiary_id VARCHAR(64) NOT NULL,
    bank_account_last4      CHAR(4),
    status                  payout_status NOT NULL DEFAULT 'scheduled',
    scheduled_for           TIMESTAMPTZ NOT NULL,
    paid_at                 TIMESTAMPTZ,
    failure_reason          TEXT,
    raw_webhook_jsonb       JSONB,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_payouts_guide_status ON payouts(guide_user_id, status, scheduled_for);
CREATE UNIQUE INDEX uq_payouts_per_payment ON payouts(payment_id);

-- =========================================================================
-- REVIEWS (bilateral, post-completion)
-- =========================================================================
CREATE TABLE reviews (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_request_id  UUID NOT NULL REFERENCES service_requests(id) ON DELETE CASCADE,
    author_user_id      UUID NOT NULL REFERENCES users(id),
    subject_user_id     UUID NOT NULL REFERENCES users(id),
    direction           review_direction NOT NULL,
    rating              SMALLINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    title               VARCHAR(120),
    body                TEXT,
    is_visible          BOOLEAN NOT NULL DEFAULT FALSE,   -- hidden until both sides submitted or 14d
    submitted_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT review_author_not_subject CHECK (author_user_id <> subject_user_id),
    CONSTRAINT review_unique_per_direction UNIQUE (service_request_id, direction)
);
CREATE INDEX idx_reviews_subject ON reviews(subject_user_id, is_visible, submitted_at DESC);

-- =========================================================================
-- MESSAGES (with translation fields)
-- =========================================================================
CREATE TABLE messages (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    connection_id       UUID NOT NULL REFERENCES connections(id) ON DELETE CASCADE,
    sender_user_id      UUID NOT NULL REFERENCES users(id),
    kind                message_kind NOT NULL DEFAULT 'text',
    body_original       TEXT,
    body_lang           VARCHAR(10),                  -- BCP-47
    body_translated     TEXT,                         -- machine-translated
    translated_lang     VARCHAR(10),
    translation_engine  VARCHAR(32),                  -- e.g. 'tencent_tmt'
    media_url           TEXT,
    read_at             TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_messages_conn_time ON messages(connection_id, created_at);

-- =========================================================================
-- CONSENT RECORDS (PIPL compliance)
-- =========================================================================
CREATE TABLE consent_records (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    scope               consent_scope NOT NULL,
    policy_version      VARCHAR(20)   NOT NULL,
    granted             BOOLEAN       NOT NULL,
    ip_address          INET,
    user_agent          TEXT,
    locale              VARCHAR(10),
    granted_at          TIMESTAMPTZ   NOT NULL DEFAULT now(),
    revoked_at          TIMESTAMPTZ
);
CREATE INDEX idx_consent_user_scope ON consent_records(user_id, scope, granted_at DESC);

-- =========================================================================
-- AUDIT LOG (append-only; immutable)
-- =========================================================================
CREATE TABLE audit_log (
    id              BIGSERIAL PRIMARY KEY,
    occurred_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    actor_kind      audit_actor NOT NULL,
    actor_user_id   UUID REFERENCES users(id),
    action          VARCHAR(80) NOT NULL,             -- e.g. 'service_request.accept'
    entity_type     VARCHAR(40) NOT NULL,
    entity_id       UUID,
    request_id      UUID,                             -- correlation id
    ip_address      INET,
    user_agent      TEXT,
    payload_jsonb   JSONB NOT NULL DEFAULT '{}'::jsonb,
    prev_hash       BYTEA,                            -- chain hash for tamper-evidence
    row_hash        BYTEA NOT NULL
);
CREATE INDEX idx_audit_entity ON audit_log(entity_type, entity_id, occurred_at DESC);
CREATE INDEX idx_audit_actor  ON audit_log(actor_user_id, occurred_at DESC);

-- Enforce append-only at DB level
CREATE RULE audit_log_no_update AS ON UPDATE TO audit_log DO INSTEAD NOTHING;
CREATE RULE audit_log_no_delete AS ON DELETE TO audit_log DO INSTEAD NOTHING;

-- =========================================================================
-- TRIGGERS: updated_at
-- =========================================================================
CREATE OR REPLACE FUNCTION set_updated_at() RETURNS trigger AS $$
BEGIN NEW.updated_at = now(); RETURN NEW; END $$ LANGUAGE plpgsql;

DO $$ DECLARE t TEXT;
BEGIN
  FOR t IN SELECT unnest(ARRAY[
    'users','tourist_profiles','guide_profiles','guide_listings',
    'service_requests','payments','payouts'])
  LOOP
    EXECUTE format('CREATE TRIGGER trg_%I_updated BEFORE UPDATE ON %I
                    FOR EACH ROW EXECUTE FUNCTION set_updated_at();', t, t);
  END LOOP;
END $$;
```

---

## 2. API Endpoints (v1)

**Conventions**
- Base: `https://api.ctrip-guides.cn/api/v1`
- Auth header: `Authorization: Bearer <access_token>` (JWT, 15-min TTL; refresh 30-day)
- All timestamps ISO 8601 UTC; money as `{amount:string, currency:string}` (string to preserve precision)
- Error envelope: `{ "error": { "code": "STRING", "message": "...", "field_errors": {...} } }`

### 2.1 `POST /api/v1/auth/register`

**Auth:** none

**Request:**
```json
{
  "role": "tourist | guide",
  "email": "user@example.com",
  "phone_e164": "+8613800138000",
  "password": "min 12 chars, 1 upper, 1 digit, 1 symbol",
  "locale": "en-US",
  "consents": [
    { "scope": "pipl_personal_data",  "policy_version": "2026-01-01", "granted": true },
    { "scope": "pipl_cross_border",   "policy_version": "2026-01-01", "granted": true }
  ]
}
```

**Response 201:**
```json
{
  "user_id": "uuid",
  "role": "tourist",
  "status": "pending",
  "verification": { "email_required": true, "phone_required": false }
}
```

**Errors:** 409 `EMAIL_TAKEN` / `PHONE_TAKEN`; 400 `WEAK_PASSWORD`, `MISSING_REQUIRED_CONSENT`

---

### 2.2 `POST /api/v1/auth/login`

**Auth:** none

**Request:**
```json
{
  "identifier": "user@example.com | +8613800138000",
  "password": "..."
}
```

**Response 200:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 900,
  "user": {
    "id": "uuid",
    "role": "tourist",
    "status": "active",
    "locale": "en-US"
  }
}
```

**Errors:** 401 `INVALID_CREDENTIALS`; 403 `ACCOUNT_SUSPENDED`

---

### 2.3 `GET /api/v1/guides`

**Auth:** optional (results identical, but personalization applied if present)

**Query params:**
| param | type | description |
|---|---|---|
| `city` | string | required for ranking; e.g. `Beijing` |
| `lang` | csv of BCP-47 | e.g. `en-US,fr-FR` |
| `date` | ISO date | service date; filters by availability |
| `specialties` | csv | e.g. `history,food` |
| `min_rating` | float 0–5 | |
| `max_price` | number | upper bound (in `currency`) |
| `currency` | ISO 4217 | display currency, default `USD` |
| `lat`,`lng` | float | optional proximity ranking |
| `sort` | enum | `relevance` (default) \| `rating` \| `price_asc` \| `price_desc` |
| `page`,`page_size` | int | default 1, 20; max 50 |

**Response 200:**
```json
{
  "page": 1, "page_size": 20, "total": 137,
  "items": [
    {
      "guide_user_id": "uuid",
      "display_name": "Li Wei",
      "avatar_url": "https://...",
      "languages": ["en-US","zh-CN"],
      "service_cities": ["Beijing"],
      "specialties": ["history","calligraphy"],
      "rating_avg": 4.87,
      "rating_count": 142,
      "response_rate_pct": 96,
      "starts_from": { "amount": "320.00", "currency": "CNY", "display": { "amount": "44.50", "currency": "USD" }, "unit": "per_half_day" },
      "featured_listing_id": "uuid",
      "score": 0.913
    }
  ]
}
```

---

### 2.4 `GET /api/v1/guides/{id}`

**Auth:** optional

**Path:** `id` = `guide_user_id`

**Response 200:**
```json
{
  "guide_user_id": "uuid",
  "display_name": "Li Wei",
  "bio": "...",
  "avatar_url": "https://...",
  "intro_video_url": "https://...",
  "languages": ["en-US","zh-CN"],
  "service_cities": ["Beijing","Tianjin"],
  "specialties": ["history","calligraphy"],
  "years_experience": 7,
  "rating_avg": 4.87,
  "rating_count": 142,
  "response_rate_pct": 96,
  "response_time_minutes": 22,
  "verified": { "license": true, "issued_on": "2019-03-12", "expires_on": "2027-03-11" },
  "listings": [
    {
      "id": "uuid",
      "title": "Half-day Forbidden City deep-dive",
      "summary": "...",
      "city": "Beijing",
      "price": { "amount": "320.00", "currency": "CNY", "unit": "per_half_day" },
      "languages": ["en-US"],
      "min_duration_hours": 4.0,
      "max_group_size": 6,
      "cover_image_url": "https://...",
      "gallery_urls": ["..."],
      "status": "published"
    }
  ],
  "availability_preview": [
    { "starts_at": "2026-06-01T01:00:00Z", "ends_at": "2026-06-01T05:00:00Z" }
  ]
}
```

**Errors:** 404 `GUIDE_NOT_FOUND`

---

### 2.5 `POST /api/v1/guides/{id}/service-request`

**Auth:** required; role `tourist`

**Path:** `id` = `guide_user_id`

**Request:**
```json
{
  "listing_id": "uuid | null",
  "service_date": "2026-06-01",
  "starts_at": "2026-06-01T01:00:00Z",
  "ends_at":   "2026-06-01T05:00:00Z",
  "party_size": 2,
  "language": "en-US",
  "tourist_notes": "We're interested in Ming dynasty history."
}
```

**Server-side computed fields:**
- `quoted_amount` ← `listing.price_amount` (if `listing_id`) or guide default rate
- `quoted_currency` ← `listing.price_currency`
- `platform_fee_pct` ← `12.00`
- `platform_fee_amount` = round(`quoted_amount` × 0.12, 2)
- `guide_payout_amount` = `quoted_amount` − `platform_fee_amount`

**Response 201:**
```json
{
  "service_request_id": "uuid",
  "status": "pending",
  "quoted": { "amount": "320.00", "currency": "CNY" },
  "platform_fee": { "amount": "38.40", "currency": "CNY", "pct": "12.00", "label_zh": "信息服务费" },
  "guide_payout": { "amount": "281.60", "currency": "CNY" },
  "expires_at": "2026-05-23T00:00:00Z"
}
```

**Errors:** 404 `GUIDE_NOT_FOUND`; 409 `GUIDE_UNAVAILABLE`; 422 `INVALID_TIME_RANGE`; 403 `GUIDE_NOT_VERIFIED`

---

### 2.6 `GET /api/v1/service-requests/mine`

**Auth:** required (works for both `tourist` and `guide`; perspective inferred from JWT role)

**Query params:**
| param | type | description |
|---|---|---|
| `status` | csv of `request_status` | optional |
| `from`,`to` | ISO date | filter by `service_date` |
| `page`,`page_size` | int | default 1, 20 |

**Response 200:**
```json
{
  "page": 1, "page_size": 20, "total": 5,
  "items": [
    {
      "id": "uuid",
      "counterparty": {
        "user_id": "uuid",
        "display_name": "Li Wei",
        "avatar_url": "https://...",
        "role": "guide"
      },
      "listing_id": "uuid",
      "service_date": "2026-06-01",
      "starts_at": "2026-06-01T01:00:00Z",
      "ends_at":   "2026-06-01T05:00:00Z",
      "party_size": 2,
      "language": "en-US",
      "status": "accepted",
      "quoted": { "amount": "320.00", "currency": "CNY" },
      "platform_fee": { "amount": "38.40", "currency": "CNY" },
      "guide_payout": { "amount": "281.60", "currency": "CNY" },
      "connection_id": "uuid | null",
      "payment_status": "initiated | captured | null",
      "created_at": "2026-05-20T03:21:00Z"
    }
  ]
}
```

---

### 2.7 `POST /api/v1/reviews`

**Auth:** required; author must be a party to the referenced `service_request` whose status is `completed`

**Request:**
```json
{
  "service_request_id": "uuid",
  "rating": 5,
  "title": "Outstanding guide",
  "body": "Knowledgeable, punctual, excellent English."
}
```

**Server-side:**
- `direction` derived from author's role
- `subject_user_id` derived from the other party in the request
- `is_visible` becomes TRUE when both directions exist OR 14 days post-completion (cron)

**Response 201:**
```json
{
  "review_id": "uuid",
  "direction": "tourist_to_guide",
  "rating": 5,
  "is_visible": false,
  "submitted_at": "2026-06-02T10:11:00Z"
}
```

**Errors:** 403 `NOT_PARTY_TO_REQUEST`; 409 `REVIEW_ALREADY_SUBMITTED`; 422 `REQUEST_NOT_COMPLETED`

---

## 3. Matching Algorithm — Guide Search Ranking

```python
# app/services/guide_search.py
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import select, and_, func
from sqlalchemy.dialects.postgresql import ARRAY

# Tunable weights (sum ~= 1.0). Stored in Redis hash `cfg:rank:weights` for live tuning.
W_LANG       = 0.28   # exact language match
W_CITY       = 0.18   # serves requested city
W_RATING     = 0.18   # bayesian-smoothed rating
W_SPECIALTY  = 0.12   # specialty overlap (Jaccard)
W_RESPONSE   = 0.08   # response rate + speed
W_AVAIL      = 0.10   # has availability on requested date
W_PRICE_FIT  = 0.06   # within budget envelope

BAYES_PRIOR_RATING = Decimal("4.30")
BAYES_PRIOR_VOTES  = 20


@dataclass
class SearchQuery:
    city: str
    languages: list[str]
    service_date: Optional[date] = None
    specialties: list[str] = None
    min_rating: Optional[float] = None
    max_price_cny: Optional[Decimal] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    sort: str = "relevance"


def search_guides(db, q: SearchQuery, page: int, page_size: int):
    # 1. HARD FILTERS in SQL — keeps the candidate set bounded
    stmt = (
        select(GuideProfile, User)
        .join(User, User.id == GuideProfile.user_id)
        .where(
            User.status == "active",
            GuideProfile.kyc_status == "approved",
            GuideProfile.guide_license_expires_on > func.current_date(),
            GuideProfile.service_cities.op("&&")(ARRAY([q.city])),
        )
    )
    if q.languages:
        stmt = stmt.where(GuideProfile.languages.op("&&")(ARRAY(q.languages)))
    if q.min_rating is not None:
        stmt = stmt.where(GuideProfile.rating_avg >= q.min_rating)
    if q.service_date is not None:
        # at least one non-blocked availability slot intersecting the date
        stmt = stmt.where(_has_availability_subq(q.service_date))

    candidates = db.execute(stmt.limit(500)).all()  # cap candidate pool

    # 2. SOFT SCORING in Python (cheap with N<=500)
    scored = []
    for guide, user in candidates:
        s_lang      = _jaccard(set(q.languages or []), set(guide.languages))
        s_city      = 1.0 if q.city in (guide.service_cities or []) else 0.0
        s_rating    = float(_bayes_rating(guide.rating_avg, guide.rating_count)) / 5.0
        s_specialty = _jaccard(set(q.specialties or []), set(guide.specialties or []))
        s_response  = 0.6 * (guide.response_rate_pct / 100.0) + \
                      0.4 * _speed_score(guide.response_time_minutes)
        s_avail     = 1.0 if q.service_date and _has_slot(db, guide.user_id, q.service_date) else 0.5
        s_price     = _price_fit(db, guide.user_id, q.max_price_cny)

        score = (
            W_LANG      * s_lang +
            W_CITY      * s_city +
            W_RATING    * s_rating +
            W_SPECIALTY * s_specialty +
            W_RESPONSE  * s_response +
            W_AVAIL     * s_avail +
            W_PRICE_FIT * s_price
        )

        # Optional geo boost
        if q.lat is not None and q.lng is not None:
            score *= _proximity_boost(db, guide.user_id, q.lat, q.lng)

        scored.append((score, guide, user))

    # 3. SORT
    if q.sort == "rating":
        scored.sort(key=lambda r: (r[1].rating_avg, r[1].rating_count), reverse=True)
    elif q.sort == "price_asc":
        scored.sort(key=lambda r: _min_price_cny(db, r[1].user_id) or Decimal("Infinity"))
    elif q.sort == "price_desc":
        scored.sort(key=lambda r: _min_price_cny(db, r[1].user_id) or Decimal(0), reverse=True)
    else:  # relevance
        scored.sort(key=lambda r: r[0], reverse=True)

    # 4. PAGINATE + project DTO
    total = len(scored)
    start = (page - 1) * page_size
    page_items = scored[start : start + page_size]
    return total, [_to_card(score, g, u) for score, g, u in page_items]


# --- helpers ---------------------------------------------------------------

def _jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)

def _bayes_rating(avg: Decimal, n: int) -> Decimal:
    # Smooth small-N guides toward platform prior
    return (BAYES_PRIOR_VOTES * BAYES_PRIOR_RATING + n * avg) / (BAYES_PRIOR_VOTES + n)

def _speed_score(minutes: int) -> float:
    # 0 min -> 1.0; 60 min -> ~0.5; 24h -> ~0.05
    import math
    return math.exp(-minutes / 90.0)

def _price_fit(db, guide_id, max_price_cny):
    if max_price_cny is None:
        return 0.5
    min_p = _min_price_cny(db, guide_id)
    if min_p is None:
        return 0.0
    if min_p <= max_price_cny:
        return 1.0
    # graceful falloff beyond budget
    over = float((min_p - max_price_cny) / max_price_cny)
    return max(0.0, 1.0 - over)

def _proximity_boost(db, guide_id, lat, lng):
    # 1.00 inside 5km, 0.95 at 25km, asymptotic to 0.85
    km = _haversine_to_nearest_listing(db, guide_id, lat, lng)
    if km is None:
        return 1.0
    return max(0.85, 1.0 - 0.006 * km)
```

**Caching:** results keyed by `sha1(query_normalized)` in Redis with 60s TTL; invalidate guide row on profile/listing/availability mutations via `INVALIDATE guides:* WHERE city=...`.

---

## 4. Implementation Notes for Builder

- **Alembic migration order:** enums → users → tourist_profiles/guide_profiles → guide_listings → availability_slots → service_requests → connections → payments → payouts → reviews → messages → consent_records → audit_log → triggers.
- **JWT:** sign with RS256; `kid` rotated quarterly; refresh tokens stored hashed in Redis (`refresh:{user_id}:{jti}`).
- **Airwallex integration is OUT of scope for this first slice** — Builder should create the schema and stub a `PaymentService` with a `create_intent_stub()` returning a fake `airwallex_intent_id`. Webhooks come in Mission 4.
- **Platform fee constant:** expose as `settings.PLATFORM_FEE_PCT = Decimal("12.00")` — *not* DB-stored; snapshot into `service_requests.platform_fee_pct` at request time so historical fees are preserved if the rate changes.
- **Authorization:** add a FastAPI dependency `require_role("tourist")` / `require_role("guide")`; for `service-requests/mine` use `require_authenticated()` and branch on `current_user.role`.