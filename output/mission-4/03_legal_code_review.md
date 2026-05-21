# Path B Compliance Code Review

**Status: ⚠️ UNABLE TO COMPLETE REVIEW — NO CODE RECEIVED**

> **DRAFT — For attorney review. This is preliminary legal/compliance analysis, not final legal advice.**

---

## Blocker

The Builder's code submission **timed out after 300s** and no source artifacts (files, diffs, repository snapshot, or pasted code) were transmitted with this request. I cannot return `VIOLATIONS FOUND` or `CLEARED` against a payload that does not exist — doing so would be fabricating a review.

**I will not issue a synthetic `CLEARED` or speculative violations.** That would defeat the purpose of the Path B compliance gate.

---

## What I Need to Proceed

Please re-submit one of the following so I can run the actual review:

1. **Repository path** (e.g., `/home/openclaw612/.openclaw/workspace/ctrip-platform/builder-output/`)
2. **Diff / patch file** from the Builder's commit
3. **Pasted code** inline (any length — I'll chunk it)
4. **File manifest** listing what the Builder produced (schemas, routes, services)

---

## Pre-Stated Review Rubric (so you can self-check while we wait)

When the code arrives, I will scan against these Path B rules. The Builder can pre-run this checklist:

### 1. Terminology Lexicon (Path B mandated rename)

| ❌ Forbidden token | ✅ Required replacement | Why |
|---|---|---|
| `tour`, `tours`, `Tour` | `service_request`, `ServiceRequest` | Avoids 旅行社 (travel agency) licensure trigger under 《旅游法》 Art. 28 + 《旅行社条例》 Art. 6 |
| `package`, `tour_package` | `listing` | "Package tour" (包价旅游) is a regulated product — platform must not appear to assemble one |
| `booking`, `book()`, `bookings` | `connection`, `connect()`, `connections` | Reinforces intermediary/information-service posture, not principal contracting |
| `customer`, `tourist` (in DB) | `requester` or `user` | Neutral; "tourist" + "booking" together implies travel-agency relationship |
| `itinerary` (as a sold product) | `proposed_schedule` (user-authored) | Itinerary sold by platform = 包价旅游产品 |

**Search command I will run:**
```
grep -rEn '\b(tour|tours|booking|bookings|package|itinerary)\b' --include='*.{py,ts,js,sql,go,java,md}'
```

### 2. Payment Flow — Platform Must NOT Hold Funds

I will flag as **VIOLATION** any of:
- Tables/columns: `platform_balance`, `escrow_account`, `pending_payout`, `held_funds`, `wallet_balance` owned by platform entity
- Code paths that route payment to a platform-owned account before guide settlement (raises 《非金融机构支付服务管理办法》 licensure issue + 《支付业务许可证》 requirement under PBOC)
- Absence of a licensed PSP (支付宝/微信支付/银联) as the merchant of record on the guide side
- "T+N" settlement logic that implies platform custody

**Required pattern:** Direct PSP-to-guide settlement with platform taking only a separately-invoiced service fee (intermediary commission, not principal revenue).

### 3. Guide Relationship — Independent Contractor Test

I will flag as **VIOLATION** code that:
- Sets guide **prices** (e.g., `guide.price = platform.compute_price()`) — must be guide-authored
- Sets guide **schedules** / mandatory availability (e.g., `min_hours_per_week`, forced shift assignment)
- Controls **how** the guide performs the service (script enforcement, mandatory route, uniform requirement enforced in code)
- Penalties for refusing work (`decline_penalty`, `acceptance_rate_threshold` that gates account)
- Exclusivity flags (`exclusive_to_platform = true`)

Any of these convert the relationship toward **de facto labor relationship** under 《劳动合同法》 Art. 7 + 人社部发〔2021〕56号 (new-form employment guidance) and trigger social insurance + severance exposure. See also 最高法 (2023) guidance on platform worker classification.

**Acceptable patterns:** Guide-set rates, guide-set availability, platform provides discovery + comms + payment-rails only.

### 4. Data Handling — Mandatory Tables

I will flag as **VIOLATION** if either is missing:

| Required table | Purpose | Legal basis |
|---|---|---|
| `consent_records` | Per-purpose, per-user, timestamped consent with version of policy consented to; separate consents for: processing, cross-border transfer, sensitive PI, marketing | PIPL Art. 14 (specific & informed); Art. 23 (separate consent for sharing); Art. 39 (separate consent for cross-border); GDPR Art. 7 + Recital 32 |
| `audit_log` | Immutable, append-only log of access to personal info, with subject, actor, purpose, lawful basis, timestamp | PIPL Art. 51(4); 《数据安全法》 Art. 27; GDPR Art. 30 (records of processing) |

Schema minima I will check for:
- `consent_records`: `user_id, purpose, policy_version, granted_at, withdrawn_at, lawful_basis, jurisdiction`
- `audit_log`: append-only constraint (no UPDATE/DELETE grant), retention ≥ 3 years (PIPL Art. 51 + 《网络安全法》 Art. 21 → 6 months min for network logs, but PI access logs should be longer)

### 5. 广告法 Hardcoded-String Scan

I will grep all user-facing strings (i18n bundles, templates, default DB seeds, error messages, marketing copy) for the absolute-prohibition lexicon under 《广告法》 Art. 9(3) and Art. 4:

```
grep -rEn '(最佳|最好|最优|第一|唯一|顶级|极品|国家级|世界级|特供|专供|免检|包治|100%|绝对|永久|彻底根除|官方推荐|央视上榜)' \
  --include='*.{json,yaml,yml,po,properties,html,jsx,tsx,vue,md}'
```

Plus EN equivalents that get translated mechanically: `"best"`, `"#1"`, `"top-rated"` (if claim cannot be substantiated → 《反不正当竞争法》 Art. 8), `"guaranteed"`, `"official"`, `"certified by the state"`.

Special-category strings I will also screen:
- Anything implying medical/health benefit of a tour ("therapeutic", "healing") → 《广告法》 Art. 17
- Comparative claims vs. named competitors → 《反不正当竞争法》 Art. 8 + 《广告法》 Art. 13

---

## Next Step

**Builder: please re-submit the code.** If the 300s timeout was due to size, send a file tree first and I'll request specific files. If you have a git commit hash, I can read it directly from `/home/openclaw612/.openclaw/workspace/ctrip-platform/`.

Until code is received, this gate remains: **🔴 NOT CLEARED (no artifact)**.

---

*Draft compliance memo — Legal agent, Ctrip-Guides. For attorney review before reliance. Assumes PRC mainland jurisdiction for platform operations and PIPL/GDPR dual-regime for tourist PI. Statutory citations are to current (as of 2026-05-21) versions of the PRC Advertising Law (2021 rev.), PIPL (2021), Tourism Law (2018 rev.), and Labor Contract Law (2012 rev.); confirm no superseding amendments before relying.*