# Legal Review Memo — Path B Constraint Stamp

**To:** Architect
**From:** Legal (Ctrip-Guides platform)
**Re:** Path B technical spec review — pre-emptive constraint stamp
**Status:** ⚠️ **DRAFT FOR ATTORNEY REVIEW** — not final legal advice.

---

## 0. Procedural note

**The spec body did not arrive** ("Agent Architect timed out after 300s"). I cannot perform a section-by-section review of a document I do not have. Rather than block the loop, I'm issuing this as a **Path B constraint stamp** — the criteria any spec must satisfy. Re-send the spec text and I will map each finding to specific sections.

Treat the items below as *line items the spec MUST satisfy* — if any are absent or contradicted, that becomes a REQUIRED change.

---

## 1. REQUIRED CHANGES (Path B red lines — must fix before sign-off)

These are derived from 《旅行社条例》Art. 2 (defines travel agency business as招徕、组织、接待 tourists and providing related services for profit), 《旅游法》Art. 28, MCT Order No. 4, PIPL, and 《电子商务法》Art. 9. If the spec contains any of the following patterns, they MUST be changed.

### R1. Language / framing (旅行社条例 Art. 2 risk)

| If spec contains… | Must change to… | Rationale |
|---|---|---|
| `book_tour`, `bookTour()`, "Book this tour" | `request_guide_service`, "Request to connect with guide" | "Booking a tour" implies *we* sell the tour. Path B = we connect parties. |
| `tour_package`, `package_id` | `guide_service_listing`, `listing_id` | "Package" = we assembled & sold it = travel agency business. |
| `itinerary` (as a platform-owned object) | `guide_proposed_plan` (owned by guide, displayed by us) | Itineraries authored by us = organizing tours. They must be authored by the guide. |
| `our tours`, `featured tours`, "tours by Ctrip-Guides" | `guide listings`, `featured guides` | Possessive framing suggests we are the tour operator. |
| `tour_operator`, `organizer` fields | `guide` / `service_provider` | We are neither. |
| "Confirmed by Ctrip-Guides" on bookings | "Confirmed by guide [Name], facilitated via Ctrip-Guides" | We do not confirm tours; the guide does. |
| `cancel_tour` endpoint that resolves cancellation rules | `forward_cancellation_request` (guide sets cancellation policy on their listing) | Setting cancellation terms = acting as the seller. |

> **Cite:** 《旅行社条例》第2条; 《旅游法》第28条 (travel agency license required for 招徕、组织、接待旅游者).

### R2. Payment flow (custody / unlicensed payment intermediation risk)

| Required | Rationale |
|---|---|
| **No platform-held escrow without a 支付牌照 (Payment Business License)** or partnership with a licensed PSP (e.g., Alipay/WeChat Pay/UnionPay) acting as the regulated escrow. Spec must name the licensed PSP. | 《非金融机构支付服务管理办法》— holding tourist funds = "备付金" = requires payment license. |
| **Funds must flow tourist → licensed PSP → guide**, with platform receiving only its information-service fee from a separate ledger entry. Spec must show this as two transactions, not platform-as-merchant-of-record. | Path B requires we are *not* the merchant of record for the tour. |
| **Fee labeling**: platform fee must be labeled "信息服务费 / Information Service Fee" — NOT "佣金/commission" or "tour booking fee" | "Commission on tour sales" looks like travel-agency revenue under 旅行社条例 Art. 2. |
| **Refund logic**: spec must route refund decisions to the guide; platform can facilitate but must not unilaterally decide tour refunds (only platform-fee refunds). | Deciding refunds on the tour itself = exercising operator authority. |
| **Settlement T+N must be ≤ duration where funds qualify as platform "暂收款"**; ideally PSP custody, platform never touches principal. Spec must specify. | Custody >7 days without license is high-risk. |

> **Cite:** 《非银行支付机构条例》(2023); PBOC 《支付业务许可证》regime.

### R3. Data model (organizing-tours signals)

The schema must **not** include any of the following as platform-owned entities:
- `Tour` / `TourPackage` / `Itinerary` (as platform records)
- `TourOperator`
- `GroupBooking` with platform as organizer
- `TourGuideAssignment` (platform-side assignment logic)

**Required schema framing (Path B compliant):**
```
GuideListing { listing_id, guide_id, title, description, price, ... }   // guide-authored content
ServiceRequest { request_id, tourist_id, listing_id, status, ... }      // intent to connect
Connection { connection_id, tourist_id, guide_id, ... }                 // facilitated match
```
Anything that aggregates multiple tourists under a platform-authored plan must be deleted or moved to the guide's authorship.

### R4. Guide relationship (independent contractor preservation)

The spec MUST NOT contain:
- `work_schedule` set by platform
- `mandatory_uniform`, `mandatory_training` flags as platform requirements (training may be *offered*, not *required*)
- `exclusivity` clauses (no "guides may only work via Ctrip-Guides")
- `kpi_score`, `performance_review` cycles that mirror employee evaluation
- Platform-set tour pricing (guide must set their own price)
- `hours_worked` tracking for compensation purposes
- Tax withholding *as employer* (platform may withhold *individual income tax under labor-service category* per 个人所得税法, but spec must label as 劳务报酬, not 工资薪金)

**Required:**
- Spec must include a `guide_self_set_price` field
- Spec must allow guides to accept/decline each request
- Spec must allow guides to list on competing platforms (no enforcement field)
- Guide onboarding must require uploading their own 导游证 (Tourist Guide License) — platform verifies, does not issue

> **Cite:** 《劳动合同法》Art. 7 (employment relationship factors); 最高人民法院关于审理劳动争议案件适用法律若干问题的解释 — control test, integration test, economic dependence test.

### R5. PIPL minimum (must appear in spec)

The spec MUST include the following technical capabilities — if any are missing, that is a REQUIRED change:

| Capability | PIPL article | Spec requirement |
|---|---|---|
| Granular consent capture (separate consent for: account creation, sensitive PI, cross-border transfer, marketing) | PIPL Art. 13, 14, 29, 39 | Consent UI flow + `consent_records` table with timestamp, version, scope |
| Sensitive PI flag (passport numbers, biometrics, location < city granularity, minors) | PIPL Art. 28-32 | Field-level classification; passport = sensitive PI for foreign tourists |
| Data subject rights API: access, copy, correction, deletion, portability, withdrawal of consent | PIPL Art. 44-47 | Self-service endpoints, ≤15-day SLA |
| Data retention limits + automated deletion | PIPL Art. 19 | TTL on every PI table; default = "shortest necessary"; transaction records 3 years per MCT Order No. 4 Art. 16 |
| Breach notification workflow | PIPL Art. 57 | Incident pipeline → CAC + affected individuals "promptly" (≤72h industry norm) |
| **Cross-border transfer mechanism** (tourist data flowing to EU home country, or processing by overseas guides) | PIPL Art. 38-39 | Spec must declare ONE: (a) CAC security assessment, (b) PI Protection Certification, (c) CAC Standard Contract (备案 filing), or (d) other treaty basis. **Spec must NOT silently transfer abroad.** |
| Separate-consent UI for cross-border transfer | PIPL Art. 39 | Distinct checkbox + disclosure of overseas recipient, purpose, categories |
| PIPIA (Personal Info Protection Impact Assessment) record | PIPL Art. 55-56 | Spec must reference where PIPIA lives (required for sensitive PI + cross-border) |
| Minors under 14 — guardian consent + dedicated rules | PIPL Art. 31; 未成年人保护法 | Spec must include `is_minor` gate; default-decline if no guardian consent |
| GDPR alignment for EU tourists | GDPR Art. 6, 9, 13, 15-22, 44-49 | Lawful basis recorded per processing purpose; SCC or adequacy basis for EU→CN |

### R6. MCT Order No. 4 floor — 《在线旅游经营服务管理暂行规定》 (8 obligations)

The spec must reflect these. Mapping below — each must trace to a concrete spec section:

| # | Obligation | Article | Spec must include |
|---|---|---|---|
| 1 | **Qualification verification of suppliers (guides)** | Art. 13 | Mandatory 导游证 upload + verification before listing goes live |
| 2 | **Display of guide credentials publicly** | Art. 13 | Public profile shows verified guide license number/status |
| 3 | **Prohibit fake reviews / 刷单炒信** | Art. 14 | Review system with anti-fraud (purchase-verified reviews only; no platform editing) |
| 4 | **Prohibit big-data discriminatory pricing (大数据杀熟)** | Art. 15 | No user-specific price differentiation for same listing/time |
| 5 | **Transaction record retention ≥ 3 years** | Art. 16 | Data retention spec ≥ 3 years for orders, payments, communications |
| 6 | **Emergency response plan for tourist safety incidents** | Art. 18-19 | 24/7 incident hotline + incident workflow; SOS button in app |
| 7 | **Personal information protection** | Art. 22 | All R5 items above |
| 8 | **Complaint handling mechanism** | Art. 23 | In-app complaint endpoint, response SLA, escalation to文旅部 12301 hotline reference |

> Additional MCT Order No. 4 items the spec should also reflect (treat as required floor):
> - Art. 7: real-name registration of users
> - Art. 8: clear, prominent display of operator info on platform
> - Art. 17: do not force-bundle products without consent

---

## 2. RECOMMENDED CHANGES (should fix)

### S1. Defensive framing
- Add a footer / API doc note: "Ctrip-Guides operates as an *information service provider* connecting tourists with independently licensed tour guides. Ctrip-Guides does not organize, arrange, or sell tours within the meaning of 旅行社条例 Art. 2."
- Place equivalent disclaimer in ToS, Privacy Policy, and at point of guide engagement.

### S2. Audit-trail richness
- Log every state transition (request → match → confirm → service-rendered → settled) with actor (tourist / guide / system) — this evidences our information-broker role.
- Retain consent version + UI screenshot hash to defend consent validity under PIPL Art. 14.

### S3. Guide pricing transparency
- Display "Price set by guide" label next to every listing price.
- Avoid platform "suggested price" features — drifts toward price-setter role.

### S4. Geographic data minimization
- Collect tourist passport data only at the point legally required (e.g., guide needs it for某些景区实名预约). Avoid bulk passport storage at signup.
- If real-time location sharing is included, default OFF; opt-in per session only (PIPL Art. 28 sensitive PI + consent).

### S5. GDPR-specific
- For EU tourists, surface lawful basis per purpose at signup; do not bundle.
- Provide EU representative contact (GDPR Art. 27) if processing EU residents — add to ToS/Privacy Policy.

### S6. Insurance hooks (not legally mandatory but reduces operator-creep risk)
- Spec should expose a field where guides attest to their own occupational/liability insurance — platform does not bundle insurance (bundling = looks like tour operator).
- If insurance offered, must be sold by a *licensed broker* via a clearly separate flow.

### S7. Marketing copy compliance hooks (《广告法》)
- Spec should include a content-screening module for guide-authored listings against 广告法 Art. 9 absolute terms (最/第一/唯一/顶级/国家级/特供). Auto-flag, do not auto-publish.
- Spec should block claims like "guaranteed best price", "100% satisfaction", "official partner of [scenic area]" without proof.

### S8. Algorithmic recommendation
- If spec includes recommender/ranking, add a "no personalized pricing" assertion + an algorithmic-transparency disclosure (per《互联网信息服务算法推荐管理规定》Art. 16, 17, 21).
- User must be able to disable personalized recommendations (Art. 17).

---

## 3. Open questions / jurisdictional flags

1. **Payment license**: Has product confirmed which licensed PSP holds custody? Without this answer I cannot fully clear R2.
2. **Foreign-guide scenarios**: Are any guides located outside mainland China (e.g., Chinese-speaking guides in HK/Macau/overseas)? If yes, cross-border data flow + foreign-talent labor rules attach.
3. **Tourist nationality scope**: EU only, or also CCPA-state residents, UK, Japan (APPI), Korea (PIPA)? Each adds incremental requirements.
4. **Platform jurisdiction of incorporation**: Are we WFOE in CN, or offshore parent? Affects PIPL Art. 3 extraterritorial application and licensing posture.
5. **Use of AI matching or content**: If guides' bios are AI-generated/translated, 《生成式人工智能服务管理暂行办法》(2023) applies — spec must include labeling.

---

## 4. Suggested next loop

Re-send the spec text (or a link/path I can read) and I will:
1. Map each REQUIRED/RECOMMENDED item above to specific spec sections by line.
2. Produce concrete redline text for offending fields/endpoints/UI strings.
3. Emit a single-page sign-off sheet the Architect can attach to the PR.

---

**Reminder:** This memo is a **DRAFT for outside-counsel review**. Citations to PIPL, 旅行社条例, 旅游法, MCT Order No. 4, 电子商务法, 广告法, and GDPR are provided for reference; final article-by-article verification against current (2026-05-21) text must be done by licensed counsel before launch.