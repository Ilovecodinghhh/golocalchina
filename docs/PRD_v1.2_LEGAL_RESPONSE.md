# PRD v1.2 — Architect Response to Legal Compliance Memo

**To:** Legal, Orchestrator, Researcher, Builder
**From:** Architect
**Date:** 2026-05-21
**Re:** Incorporating Legal compliance memo (PIPL / 广告法 / 旅游法 / cross-border / contractor classification) into PRD and architecture
**Status:** PRD v1.1 → v1.2; Builder unblocked for **data-model + consent + DSR + agency-partner** workstreams. Two items (C-01 licensing path, codename vs production brand) remain BLOCKED on Business/Legal decisions and are flagged below.

---

## 0. Executive Summary of Architectural Changes

| Legal Item | Rating | Architect Action | Builder Status |
|---|---|---|---|
| C-01 Travel-agency licensing path (own vs partner) | 🔴 | Designing for **Path B + C hybrid** (partner 旅行社 + pilot cities only). All booking writes require `travel_agency_partner_id`. Awaiting Business sign-off. | **BLOCKED on business decision**, but schema can be built now |
| C-02 Pilot-city legal map | 🔴 | MVP city list **conditional**: ship only cities cleared by Legal. Geo-fence in code. | Schema includes `city.regulatory_status` |
| C-03 CAC Standard Contract | 🔴 | Architect: monitor counters & lifecycle hooks; Legal owns filings. | Counters built into telemetry |
| C-04 GDPR SCC + TIA | 🔴 | Architect: keep transfer log + vendor inventory; Legal owns SCC. | Schema ready |
| C-05 Separate-consent UX | 🔴 | New consent-gating component, **separate checkboxes per purpose**. Full spec in §3. | **Builder unblocked** |
| C-06 Consent ledger table | 🔴 | Full DDL in §2. | **Builder unblocked** |
| C-07 DSR workflow (PIPL+GDPR) | 🔴 | New service `dsr-service` with 5 endpoints. Full spec in §4. | **Builder unblocked** |
| C-08 Retention schedule | 🟡 | `retention_until` column on every PI table + nightly purge job. | **Builder unblocked** |
| C-09 Vendor inventory | 🟡 | Static `vendors.yaml` + DB-backed `vendor_inventory` view. | **Builder unblocked** |
| C-10 PRC data localization | 🔴 | Primary datastore = Alibaba Cloud (cn-hangzhou); cross-border egress via single gateway service. | **Builder unblocked** |
| C-11 Marketing copy screening | 🟡 | New middleware `adcopy-screen`. Blocklist + regex pipeline. Spec in §6. | **Builder unblocked** |
| C-12 "100% verified" claim | 🟡 | PRD copy rephrased (see §1.4). | Done in this doc |
| C-13 Guide ToS / IC structure | 🟡 | Removed "assign", "shift", "manager" from UI lexicon. Glossary in §7. | **Builder unblocked** |
| C-14 Algorithmic ranking transparency | 🟡 | Add `/discovery/ranking-explanation` endpoint + UI tooltip. | **Builder unblocked** |
| C-15 Children's data | 🟡 | Age gate at signup; if minor flagged in booking party, surface guardian consent UI. | **Builder unblocked** |
| C-17 Discriminatory-deactivation guard | 🟡 | Deactivation events tied to objective trigger types (enum). | **Builder unblocked** |
| C-19 Tax withholding | 🟡 | Payout pipeline emits 劳务报酬 withholding statements (see §5). | **Builder unblocked** |
| C-20 Bilingual ToS / PP | 🟡 | i18n keys reserved; Legal supplies copy. | Builder reserves keys |
| Brand "Ctrip-Guides" assumption #3 | 🔴 | **HARD STOP for production brand**. Internal codename only in code; production brand TBD. | Codename `ctrip_guides` retained for repo only |

Net effect: **MVP date unchanged** if Business decides C-01 and brand within 5 business days; **+3 weeks** for consent ledger + DSR service (parallelizable with city onboarding).

---

## 1. PRD Revisions

### 1.1 MVP Cities (revised)

- **MVP geographic scope is now conditional**, not a fixed list.
- Pre-launch, Legal supplies a list of `(city, free_practice_pilot_status, partner_agency_required)` tuples → stored in `city_regulatory_config` table.
- Code geo-fences booking creation by `city.regulatory_status IN ('FREE_PRACTICE_PILOT', 'PARTNER_AGENCY_OK')`.

### 1.2 Booking Model (revised)

- Every `Booking` now has a non-null `travel_agency_partner_id` (FK).
- If city is `FREE_PRACTICE_PILOT` and guide has `self_practice_eligible=true`, `travel_agency_partner_id` may point to a synthetic "self-practice" partner row with `kind='SELF_PRACTICE'`.
- Otherwise it must point to a `kind='LICENSED_AGENCY'` partner.

### 1.3 Sensitive PI Inventory (binding on data model)

| Field | Sensitive under PIPL? | Storage |
|---|---|---|
| `passport_no` / `id_card_no` | Yes | Encrypted at rest (SM4 for PRC store; AES-256-GCM for global mirror) + access audit |
| `payment_token` | Yes (financial) | Tokenized only; never store PAN |
| `precise_location` | Yes (location) | Stored only during active booking; purged 30 days after completion |
| `country` | Yes (basis: ethnic/national category implied) | Encrypted at rest |
| `face_image` (KYC for guide) | Yes (biometric) | Stored only as hash + lifecycle-bound original; SM4 encrypted |
| `health_notes` (allergies in itinerary) | Yes (health) | Encrypted at rest; default off in UI |

All sensitive fields carry `requires_separate_consent=true` metadata used by serializers (see §2.3).

### 1.4 Marketing Copy Changes

| Old | New |
|---|---|
| "Verify **100%** of guides hold valid 持证导游 credentials" | "All guides on the platform must hold a valid 持证导游 card; we verify before activation and re-verify on expiry." |
| "Frictionless cross-border booking" | (kept; internal goal only — explicitly tagged `internal_only=true` in `goals.yaml`) |
| "Tourist completes book + pay in <3 minutes" | Internal performance target; not consumer copy. Tagged `internal_only=true`. |

A consumer-copy linter (§6) refuses to publish any string containing the old wording.

---

## 2. Data Model — Compliance-Driven Additions

### 2.1 New Tables

```sql
-- C-06: per-purpose consent ledger
CREATE TABLE consent_event (
  id              BIGSERIAL PRIMARY KEY,
  user_id         BIGINT NOT NULL REFERENCES "user"(id),
  purpose_code    VARCHAR(64) NOT NULL,       -- e.g. 'PROCESS_BOOKING','CROSS_BORDER_TO_STRIPE'
  policy_version  VARCHAR(32) NOT NULL,       -- e.g. 'pp-2026-05-21-v1'
  granted_at      TIMESTAMPTZ,
  revoked_at      TIMESTAMPTZ,
  evidence_hash   CHAR(64) NOT NULL,          -- SHA-256 over (ip, ua, screen_id, ts, locale)
  ip_addr         INET NOT NULL,
  user_agent      TEXT NOT NULL,
  locale          VARCHAR(10) NOT NULL,
  separate_consent BOOLEAN NOT NULL DEFAULT FALSE  -- true if this consent was collected via separate checkbox (PIPL Art. 29)
);
CREATE INDEX ix_consent_user_purpose ON consent_event(user_id, purpose_code);

-- C-04 / C-10: cross-border transfer log
CREATE TABLE cross_border_transfer_log (
  id              BIGSERIAL PRIMARY KEY,
  occurred_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
  subject_user_id BIGINT REFERENCES "user"(id),  -- nullable for aggregated transfers
  vendor_code     VARCHAR(64) NOT NULL,           -- FK-ish to vendors.yaml
  destination_country CHAR(2) NOT NULL,           -- ISO-3166-1 alpha-2
  purpose_code    VARCHAR(64) NOT NULL,
  lawful_basis    VARCHAR(32) NOT NULL,           -- 'SEPARATE_CONSENT','CAC_STANDARD_CONTRACT','SECURITY_ASSESSMENT'
  data_categories TEXT[] NOT NULL,                -- ['name','contact','itinerary','payment_token']
  record_count    INTEGER NOT NULL DEFAULT 1,
  consent_event_id BIGINT REFERENCES consent_event(id)
);
CREATE INDEX ix_xfer_subject ON cross_border_transfer_log(subject_user_id);
CREATE INDEX ix_xfer_vendor_time ON cross_border_transfer_log(vendor_code, occurred_at);

-- C-03 counters: materialized view refreshed nightly
-- (counts PI subjects exported per calendar year for CAC threshold tracking)

-- C-01: travel agency partner
CREATE TABLE travel_agency_partner (
  id              BIGSERIAL PRIMARY KEY,
  kind            VARCHAR(24) NOT NULL,           -- 'LICENSED_AGENCY','SELF_PRACTICE'
  legal_name_cn   VARCHAR(256),
  license_no      VARCHAR(64),                    -- 旅行社业务经营许可证 number
  license_expiry  DATE,
  contact_email   VARCHAR(255),
  api_callback_url TEXT,                          -- for dispatch confirmation
  active          BOOLEAN NOT NULL DEFAULT TRUE,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- C-02: city regulatory config
CREATE TABLE city_regulatory_config (
  city_code           VARCHAR(16) PRIMARY KEY,
  regulatory_status   VARCHAR(32) NOT NULL,       -- 'FREE_PRACTICE_PILOT','PARTNER_AGENCY_OK','BLOCKED'
  partner_required    BOOLEAN NOT NULL,
  effective_from      DATE NOT NULL,
  legal_memo_ref      TEXT
);

-- C-07: DSR requests
CREATE TABLE dsr_request (
  id              BIGSERIAL PRIMARY KEY,
  user_id         BIGINT NOT NULL REFERENCES "user"(id),
  kind            VARCHAR(16) NOT NULL,           -- 'ACCESS','EXPORT','CORRECT','DELETE','OBJECT_ADM','RESTRICT'
  regime          VARCHAR(8)  NOT NULL,           -- 'PIPL','GDPR','BOTH'
  status          VARCHAR(16) NOT NULL DEFAULT 'OPEN',  -- OPEN/IN_PROGRESS/DONE/REJECTED
  due_by          TIMESTAMPTZ NOT NULL,           -- 15d for PIPL, 30d for GDPR (strict superset = 15d)
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  fulfilled_at    TIMESTAMPTZ,
  notes           TEXT
);

-- C-17: deactivation audit
CREATE TABLE guide_deactivation_event (
  id              BIGSERIAL PRIMARY KEY,
  guide_id        BIGINT NOT NULL REFERENCES guide_profile(id),
  trigger_type    VARCHAR(48) NOT NULL,           -- enum: 'LICENSE_EXPIRED','LICENSE_REVOKED','SAFETY_VIOLATION_CONFIRMED','LEGAL_ORDER','SELF_REQUESTED'
  evidence_uri    TEXT,                           -- pointer to objective evidence
  reviewed_by     BIGINT REFERENCES staff_user(id),
  reactivated_at  TIMESTAMPTZ,
  occurred_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- C-19: tax withholding statements
CREATE TABLE guide_withholding_statement (
  id              BIGSERIAL PRIMARY KEY,
  guide_id        BIGINT NOT NULL REFERENCES guide_profile(id),
  period_yyyymm   CHAR(6) NOT NULL,
  gross_cny       NUMERIC(12,2) NOT NULL,
  withheld_cny    NUMERIC(12,2) NOT NULL,
  net_cny         NUMERIC(12,2) NOT NULL,
  statement_uri   TEXT,                           -- PDF in OSS
  filed_at        TIMESTAMPTZ
);

-- C-15: minor traveler flag (per-party-member)
ALTER TABLE booking_party_member
  ADD COLUMN is_minor BOOLEAN NOT NULL DEFAULT FALSE,
  ADD COLUMN guardian_consent_event_id BIGINT REFERENCES consent_event(id);
```

### 2.2 Modifications to Existing Tables

```sql
ALTER TABLE booking
  ADD COLUMN travel_agency_partner_id BIGINT NOT NULL REFERENCES travel_agency_partner(id),
  ADD COLUMN city_code VARCHAR(16) NOT NULL REFERENCES city_regulatory_config(city_code);

-- Retention on every PI table (C-08)
ALTER TABLE tourist_profile
  ADD COLUMN retention_until TIMESTAMPTZ NOT NULL DEFAULT (now() + INTERVAL '3 years'),
  ADD COLUMN soft_deleted_at TIMESTAMPTZ;

ALTER TABLE guide_profile
  ADD COLUMN retention_until TIMESTAMPTZ NOT NULL DEFAULT (now() + INTERVAL '10 years'),  -- tax retention
  ADD COLUMN soft_deleted_at TIMESTAMPTZ;

ALTER TABLE message
  ADD COLUMN retention_until TIMESTAMPTZ NOT NULL DEFAULT (now() + INTERVAL '2 years');
```

### 2.3 Field-Level Metadata (PIPL classification)

Each ORM model declares per-field metadata used by serializers, exporters, and the consent gate:

```python
# example for tourist_profile
SENSITIVE_FIELDS = {
  'passport_no':       {'sensitive': True,  'category': 'identity',  'requires_separate_consent': True, 'encryption': 'SM4'},
  'country':           {'sensitive': True,  'category': 'national',  'requires_separate_consent': True, 'encryption': 'AES-256-GCM'},
  'precise_location':  {'sensitive': True,  'category': 'location',  'requires_separate_consent': True, 'encryption': 'AES-256-GCM', 'ttl_days': 30},
  'preferred_curr':    {'sensitive': False},
  'locale':            {'sensitive': False},
}
```

The DSR export builder reads this dict to assemble the user's portable archive.

---

## 3. Separate-Consent UX (C-05) — Builder Spec

### 3.1 Consent Purposes (canonical enum)

| `purpose_code` | When asked | Sensitive? | Cross-border? |
|---|---|---|---|
| `ACCOUNT_CREATE` | Signup | No | No |
| `PROCESS_BOOKING` | First booking | No | No |
| `STORE_PASSPORT` | Booking with PRC tour-registration requirement | **Yes** (separate) | No |
| `PROCESS_PAYMENT_STRIPE` | Booking checkout | Yes (financial) | **Yes** (US/IE) |
| `SHARE_WITH_PARTNER_AGENCY` | Booking checkout when partner-routed | No (but separate) | No |
| `USE_PRECISE_LOCATION` | First geofence operation | **Yes** (separate) | No |
| `TRANSLATE_MESSAGE_OVERSEAS` | First message translation | No | **Yes** |
| `EMAIL_VIA_SENDGRID` | Signup (notification) | No | **Yes** (US) |
| `MARKETING_EMAIL` | Settings opt-in | No | Optional |
| `GUARDIAN_FOR_MINOR` | When tourist marks party member as minor | **Yes** | Depends |

### 3.2 Component Hierarchy

```
<ConsentGate purposeCode="STORE_PASSPORT">
  <ConsentCard>
    <ConsentTitle/>                  // i18n key per purpose
    <ConsentBodyShort/>               // 2 sentences
    <ConsentBodyLong/>                // expandable
    <ConsentCheckbox required />      // single purpose only, separate
    <ConsentLink href="privacy"/>
    <ConsentRecordButton onClick={recordConsent}/>
  </ConsentCard>
</ConsentGate>
```

**Rule:** No bundling. If a screen needs N sensitive consents, render N separate `<ConsentCard>` components, each with its own checkbox and its own `consent_event` write.

### 3.3 API

```
POST /v1/consents
  body: { purpose_code, policy_version, granted: bool, screen_id }
  effect: writes consent_event row with ip/UA/locale from request
  returns: 201 { consent_event_id }

GET  /v1/consents?user_id=me
  returns: latest grant/revoke per purpose_code (for settings UI)

POST /v1/consents/:purpose_code/revoke
  effect: writes consent_event row with revoked_at=now, granted_at=NULL
```

A server-side **consent middleware** runs on every request that touches a `requires_separate_consent` field; if no active `consent_event` exists for the implied purpose, the request returns `403 ConsentRequired { missing: [purpose_code,...] }`.

---

## 4. DSR Service (C-07) — Builder Spec

### 4.1 Endpoints (auth required, MFA required for DELETE/EXPORT)

```
POST   /v1/dsr/requests
  body: { kind: 'ACCESS'|'EXPORT'|'CORRECT'|'DELETE'|'OBJECT_ADM'|'RESTRICT', regime: 'PIPL'|'GDPR'|'BOTH', payload? }
  returns: 202 { request_id, due_by }

GET    /v1/dsr/requests/:id      -> status

GET    /v1/dsr/requests/:id/archive  -> signed URL to ZIP (for EXPORT)

POST   /v1/dsr/requests/:id/cancel
```

**SLA enforced**: `due_by = created_at + 15 days` (PIPL Art. 50 effective floor; tighter than GDPR's 30d, so we use the stricter).

### 4.2 EXPORT archive layout

```
archive/
  profile.json            # all non-sensitive PI
  sensitive/
    passport.json         # if STORE_PASSPORT consent ever granted
    payment_tokens.json
    locations.json
  bookings.json
  messages.jsonl
  consents.json           # full consent_event history
  cross_border_log.json   # all xfer events for this subject
  manifest.json           # field metadata + retention table
```

### 4.3 DELETE semantics

- **Soft-delete** by default: PII anonymized in-place, `soft_deleted_at` set, retention rows still kept where law requires (tax 10y).
- **Hard-delete** scheduled when all retention obligations expire (cron).
- For booking parties, only the requesting subject's PII is anonymized; co-traveler fields are independently retained per their own consent state.

---

## 5. Cross-Border Egress Gateway (C-04, C-10) — Builder Spec

### 5.1 Service `xborder-gw`

All outbound calls to non-PRC vendors **must** go through this service. Direct outbound network calls from application containers are blocked at the VPC egress firewall.

```
POST /xb/v1/dispatch
  body: { vendor_code, subject_user_id, purpose_code, payload, data_categories }
  behavior:
    1. Look up vendor in vendor_inventory; reject if not active or not approved for purpose.
    2. Verify active consent_event for subject_user_id + purpose_code; reject if missing.
    3. Apply per-vendor PII minimization (e.g., strip passport before sending to SendGrid).
    4. Write cross_border_transfer_log row.
    5. Forward request; return upstream response.
  returns: upstream payload OR 403 ConsentRequired OR 451 VendorNotApproved
```

### 5.2 Vendor inventory schema

`vendors.yaml` (versioned in repo, mirrored to `vendor_inventory` table):

```yaml
- code: stripe_payments
  legal_name: Stripe Payments Company
  destination_country: US
  also_in: [IE]
  cac_standard_contract_filed: false   # Legal updates
  gdpr_dpa_signed: true
  scc_module: 'controller-to-processor'
  approved_purposes: [PROCESS_PAYMENT_STRIPE]
  pii_allowed: [name, email, payment_token, amount, currency]
- code: sendgrid
  legal_name: Twilio Inc.
  destination_country: US
  cac_standard_contract_filed: false
  gdpr_dpa_signed: true
  approved_purposes: [EMAIL_VIA_SENDGRID]
  pii_allowed: [email, locale, first_name]
- code: google_translate
  destination_country: US
  approved_purposes: [TRANSLATE_MESSAGE_OVERSEAS]
  pii_allowed: [message_text_redacted]   # gateway strips proper nouns
```

Builder must reject any code path that tries to call an external vendor URL not registered here.

### 5.3 Threshold counters (C-03)

Nightly job:
```
SELECT count(DISTINCT subject_user_id)
  FROM cross_border_transfer_log
  WHERE occurred_at >= date_trunc('year', now());
```
Emits Prometheus gauges `pipl_xfer_subjects_total{sensitivity}`; alerts at 80k (non-sensitive) and 8k (sensitive) — 80% of the 100k/10k Standard-Contract threshold.

---

## 6. Marketing-Copy Screening Middleware (C-11) — Builder Spec

### 6.1 Service `adcopy-screen`

```
POST /adcopy/v1/check
  body: { text, locale, channel: 'web'|'email'|'push'|'ads' }
  returns: { allowed: bool, hits: [{ term, rule_id, severity }], suggestions: [...] }
```

### 6.2 Rule sources

```
rules/
  cn_absolutist.yaml       # 最|第一|唯一|顶级|极品|最佳|最优|首选|独家|100%|绝对|包治|零风险
  cn_authority.yaml        # 国家级|特供|专供|央视推荐|政府指定
  cn_urgency.yaml          # 限时仅剩|最后\s*\d+\s*名
  en_absolutist.yaml       # \b(100%|guaranteed|risk[- ]?free|best|number one|the only)\b
  en_authority.yaml        # \b(government[- ]approved|state[- ]endorsed)\b
```

### 6.3 CI hook

A pre-commit hook + GitHub Action run `adcopy-screen` against all strings under `src/i18n/marketing/**` and fail the build on any HIGH severity hit.

---

## 7. UI/UX Glossary Change (C-13)

Banned words in product UI (replace with neutral terms):

| ❌ | ✅ |
|---|---|
| "Assign to guide" | "Propose to guide" |
| "Shift" | "Availability slot" |
| "Manager" (over guides) | "Compliance reviewer" |
| "Performance score" (penalty signal) | "Compliance score" (objective triggers only) |
| "Discipline" | "Compliance action" |

Builder enforces via an i18n string linter that flags banned tokens in `src/i18n/**` for guide-facing namespaces.

---

## 8. Algorithmic Transparency (C-14)

New endpoint:
```
GET /v1/discovery/ranking-explanation
  returns: {
    factors: [
      { code: 'language_match',  weight: 0.30, description_i18n_key: '...' },
      { code: 'specialty_match', weight: 0.25, ... },
      { code: 'distance',        weight: 0.15, ... },
      { code: 'rating',          weight: 0.15, ... },
      { code: 'price',           weight: 0.10, ... },
      { code: 'availability',    weight: 0.05, ... }
    ],
    last_updated: '2026-05-21',
    user_can_opt_out: true,
    fallback_behavior: 'alphabetical_by_distance'
  }
```
Tooltip "Why am I seeing these guides?" on the discovery screen links to a page that consumes this endpoint. User opt-out toggles a `personalization_enabled` flag on the profile that switches the ranker to deterministic fallback.

---

## 9. Children's Data (C-15)

- Signup form adds a hard age gate (DOB picker, locale-aware).
- Booking flow: when adding a party member with `is_minor=true`, render a `<ConsentGate purposeCode="GUARDIAN_FOR_MINOR">` block that collects guardian consent + guardian relationship; writes `consent_event` referenced by `booking_party_member.guardian_consent_event_id`.
- Under-14 minors trigger a **second** `<ConsentGate>` for sensitive PI (e.g., dietary/health) per PIPL Art. 31.

---

## 10. Architecture Diagram (delta)

```
                ┌───────────────────────┐
   Tourist App ─┤  api-gateway (PRC)    │── consent-mw ──┐
   Guide App   ─┤                       │                │
                └─────────┬─────────────┘                │
                          │                              │
       ┌──────────────────┼──────────────────┐           │
       ▼                  ▼                  ▼           │
   booking-svc      discovery-svc       dsr-service      │
       │                  │                  │           │
       ▼                  ▼                  ▼           │
   ┌─────────────────────────────────────────────┐       │
   │  Primary DB  (Alibaba Cloud cn-hangzhou)    │◄──────┘
   │  + consent_event, xborder_log, dsr_request  │
   └─────────────────────────────────────────────┘
                          │
                          ▼
                ┌───────────────────────┐
                │  xborder-gw           │  ← only egress path to non-PRC vendors
                │  + vendor_inventory   │
                └───────────────────────┘
                  │       │        │
                  ▼       ▼        ▼
              Stripe   SendGrid  Translate
              (US/IE)  (US)      (US)
```

---

## 11. Builder Task Breakdown (handoff)

| # | Task | Depends on | Effort |
|---|---|---|---|
| B-01 | DDL migrations for §2.1 new tables + §2.2 alters | — | M |
| B-02 | `consent-service` (POST/GET/REVOKE) + middleware | B-01 | M |
| B-03 | `<ConsentGate>` React component + 10 purpose-specific cards | B-02 | M |
| B-04 | `dsr-service` (5 endpoints) + EXPORT archive builder | B-01, B-02 | L |
| B-05 | `xborder-gw` service + `vendors.yaml` schema + DB sync | B-01 | M |
| B-06 | VPC egress firewall rules (block direct vendor calls) | B-05 | S |
| B-07 | Booking schema + UI: `travel_agency_partner_id`, `city_code` plumbing | B-01 | M |
| B-08 | `travel_agency_partner` admin CRUD + dispatch callback | B-07 | M |
| B-09 | `city_regulatory_config` admin + booking geo-fence enforcement | B-01 | S |
| B-10 | `adcopy-screen` service + CI hook | — | S |
| B-11 | i18n string linter for guide-facing banned-token glossary | — | S |
| B-12 | Discovery ranking-explanation endpoint + tooltip UI + opt-out | — | S |
| B-13 | Minor age gate + guardian consent flow | B-03 | S |
| B-14 | Deactivation event audit table wiring + admin reason picker | B-01 | S |
| B-15 | Tax withholding statement generator (劳务报酬) + cron | B-07 | M |
| B-16 | Retention purge cron (soft→hard delete state machine) | B-01 | S |
| B-17 | i18n keys reserved for bilingual ToS/PP (Legal fills copy) | — | XS |
| B-18 | Prometheus xfer threshold alerts (80k/8k) | B-05 | XS |

All B-tasks are unblocked once §11 lands except those flagged BLOCKED below.

---

## 12. Items Still BLOCKED (need Business/Legal decisions)

| # | Decision needed | Owner | Why blocking |
|---|---|---|---|
| BL-01 | Travel-agency licensing path (own license vs partner vs hybrid) | Business + Legal | Determines whether B-08 ships with real partner integrations or self-license workflow |
| BL-02 | Production brand name (Ctrip-Guides is **codename only**) | Business + Legal (trademark) | Cannot ship consumer UI / domain / app-store listing without this |
| BL-03 | MVP city legal map (which cities cleared for which path) | Legal | Code is ready; needs the actual list of cities + statuses |
| BL-04 | Engagement of PRC + EU outside counsel for sign-off on consent UX & SCC | Legal | Cannot launch without sign-off |
| BL-05 | DPO / PIPL representative appointment (if threshold-triggered) | Legal | Required pre-launch if PI > threshold |

I am proceeding to hand B-01 through B-18 to Builder **except** B-08 partner integration shells (waits on BL-01) and any consumer-brand strings (wait on BL-02).

---

## 13. Anything UNCLEAR

1. Whether Stripe is the final payment processor or whether Alipay/WeChat Pay 跨境 will be the actual rail (impacts vendor inventory + assumption #2 in Legal memo §7).
2. Whether the guide KYC face-match is in-house or via a PRC vendor (CertifAI / 旷视 etc.) — affects vendor inventory + biometric handling.
3. Whether the platform will offer occupational injury insurance (Legal C-18 recommends YES). Awaiting Ops/Finance decision; data model already supports a `guide_insurance_policy` table if green-lit.
4. Confirmation of the codename → brand transition (BL-02). Until resolved, repo identifier `ctrip_guides` remains.

---

**Next Architect action:** wait for BL-01 and BL-02 resolutions; meanwhile, Builder may proceed with B-01 through B-18 minus the blocked subtasks.
