# LEGAL ANALYSIS MEMORANDUM

**TO:** Orchestrator; Architect; Researcher; Founder
**FROM:** Legal (Ctrip-Guides Platform)
**DATE:** 2026-05-21
**RE:** Licensing Analysis — Does Ctrip-Guides Require a 旅行社业务经营许可证?
**STATUS:** 🟥 **DRAFT FOR ATTORNEY REVIEW — NOT LEGAL ADVICE**
**Privilege:** Attorney work-product preparation; do not distribute outside the core team.

---

## ⚠️ STANDING DISCLAIMERS

1. **This is a DRAFT memo prepared by in-house Legal for external counsel review.** No commercial or product decision should be made on the basis of this memo alone. Engage a PRC-qualified tourism-law firm (recommend a Beijing or Shanghai 文旅 specialist) before launch.
2. The underlying Researcher memo flagged that **web search returned 0 results this session** and all citations originate from a training corpus snapshot. **Every cited article must be re-verified against the live 国家法律法规数据库 (flk.npc.gov.cn) and 文化和旅游部 site.**
3. I have not seen the proposed Terms of Service, the guide contractor agreement, the payment-flow architecture, or the marketing copy. Conclusions may shift materially once those are reviewed.
4. Enforcement practice in China tourism law is **highly local**. Beijing, Shanghai, Xi'an (Shaanxi), and Chengdu (Sichuan) each have their own 文旅局 enforcement posture. This memo assumes uniform application; that assumption is fragile.
5. Markings throughout: ✅ verified-from-training; 🟡 inferred; 🔴 unverified — needs counsel; ❌ gap.

---

## 1. EXECUTIVE SUMMARY (GO / NO-GO)

| Question | Answer | Confidence |
|---|---|---|
| Does the **current proposed model** require a 旅行社业务经营许可证? | **🟡 Probably YES, on the face of 旅行社条例 Art. 2** — the "组织" (organize) verb arguably captures a commission-charging matchmaker. | Medium-high |
| Can the model be **restructured** to lawfully avoid the permit? | **🟢 Yes, under specific structural conditions** — but only by either (a) operating in the 导游自由执业 pilot regions with a true information-service architecture, OR (b) routing bookings through a licensed travel-agency partner. | Medium |
| Does the **2020 在线旅游经营服务管理暂行规定 (MCT Order No. 4)** apply? | **🟢 Almost certainly YES — independent of the licensing question.** It imposes platform conduct duties whether or not we hold a travel-agency permit. | High |
| Bottom-line recommendation for MVP | **DO NOT LAUNCH the current model as-is.** Adopt Path B (pilot-city information-service + non-pilot agency-partner hybrid) or Path C (full agency partner) below. | — |

**GO/NO-GO call:** 🟡 **CONDITIONAL GO.** The business is viable in China, but **not in the structure as drafted**. The single biggest unresolved risk is whether the platform itself is treated as "招徕、组织" (soliciting & organizing) tourists under 旅行社条例 Article 2 — see §3 below.

---

## 2. LEGAL FRAMEWORK — APPLICABLE INSTRUMENTS

| # | Instrument | Key articles | Effective |
|---|---|---|---|
| 1 | 中华人民共和国旅游法 (Tourism Law) | **Art. 28** (permit required to establish travel agency); **Art. 29** (outbound permit); **Art. 38** (guides must be certified, contract with agency OR through 导游服务公司); **Art. 95** (penalties — operating without permit). ✅ | 2013-10-01 (amend. 2016, 2018) |
| 2 | 旅行社条例 (Regulation on Travel Agencies), State Council Decree No. 550 | **Art. 2** (definition of 旅行社业务 — the trigger); **Art. 6–8** (capital, premises, deposit); **Art. 22** (guide-dispatch rule); **Art. 48** (penalty for unlicensed operation). ✅ | 2009 (amend. 2013, 2016, 2020) |
| 3 | 旅行社条例实施细则, MCT Order | Implementation detail on Art. 2 verbs ("招徕、组织、接待"). 🟡 — exact current order number to be re-verified by counsel. | (verify) |
| 4 | 在线旅游经营服务管理暂行规定 (MCT Order No. 4) | Platform conduct rules: real-name verification, complaint handling, "big-data discrimination" prohibition, mandatory data retention 3 years. ✅ | 2020-10-01 |
| 5 | 导游管理办法 (MCT Order No. 41) | Guide qualifications; conditions under which a guide may practice without travel-agency dispatch (pilot tie-in). ✅ | 2018-01-01 |
| 6 | 《关于开展导游自由执业试点工作的通知》 | Pilot for guides to contract directly with tourists; originally Jiangsu/Zhejiang/Shanghai/Guangdong/Jilin. 🔴 **Current pilot scope in 2025–2026 must be re-verified.** Beijing, Xi'an, Chengdu were **not in the original pilot** — this is a critical fact for our MVP city selection. | 2016 (pilot) |
| 7 | 电子商务法 | Platform operator duties (Art. 27, 38, 42); applies regardless of tourism licensing. ✅ | 2019-01-01 |
| 8 | 中华人民共和国旅游法 Art. 111 / 旅行社条例 Art. 38 | Guide dispatch & contract requirements. | — |

---

## 3. Q1 — DOES THE MODEL TRIGGER A 旅行社业务经营许可证?

### 3.1 The legal test
**旅行社条例 Article 2** defines 旅行社业务 as:

> "**招徕、组织、接待**旅游者，为其提供相关旅游服务，开展国内旅游业务、入境旅游业务或者出境旅游业务的经营活动。"

The trigger is the disjunctive set of verbs **招徕 (solicit) / 组织 (organize) / 接待 (receive)** — performed *for consideration*, on a *routine commercial basis*, in respect of *travel services*. 🟡 MCT enforcement guidance (per Researcher memo, needs re-verification 🔴) treats **any one** verb as sufficient.

### 3.2 Element-by-element application to Ctrip-Guides as drafted

| Element | Our facts | Triggered? |
|---|---|---|
| 招徕 (solicit tourists) | Platform markets to foreign tourists, runs ads, drives bookings. | 🔴 **Likely YES.** Marketing tourists to a tour-related service offering is the textbook "solicit." |
| 组织 (organize) | Platform sets the booking framework, holds payment, sets cancellation/refund rules, takes 15% commission. Tourist's commercial counterparty for the **booking transaction** is the platform, even if the **service contract** is guide↔tourist. | 🟡 **Likely YES** under functional interpretation. The line MCT has historically drawn (per Researcher 🔴) is whether the platform is the commercial counterparty for the booking — and 15% commission on every booking + custody of funds points strongly to "organizing." |
| 接待 (receive) | Platform does not meet, transport, or host tourists physically. | 🟢 NO. |
| Related tourism services | Guide service is unambiguously a tourism service. | 🔴 YES. |
| Inbound business (入境旅游业务) | Foreign tourists in China = **入境旅游**. This is the **highest-regulated tier**: 旅行社条例 Art. 6 requires a higher security deposit (140,000 RMB for inbound) and an additional inbound endorsement on the permit. ✅ | 🔴 YES — this matters a lot. |

### 3.3 Conclusion — Q1
**🟡 Probable YES.** On the plain text of Art. 2, two of three trigger verbs are likely satisfied. The "we're just a tech platform / classifieds board" defense is **available in theory** (see §3.4) but **fragile** under current structure because:

- We collect payment (custody of funds → strong "organizing" signal). 🟡
- We take a percentage commission rather than a flat listing fee (revenue scales with tourism activity → strong "operating travel business" signal). 🟡
- We market to tourists rather than letting guides self-market (this is "solicit"). 🔴
- We handle inbound foreign tourists (highest-regulated tier). ✅

### 3.4 Can we restructure to avoid Art. 2?
**🟢 Yes, conditionally.** The Researcher memo correctly identifies the four-factor information-service safe harbor (paraphrased from cross-reading 旅行社条例 Art. 2 + 电子商务法 Art. 9 — 🟡 needs counsel sign-off):

1. **Direct contract** — service contract is guide↔tourist, with the platform a non-party; ToS must say this explicitly.
2. **No holding-out** — platform never markets itself as the tour operator; marketing copy reviewed under 广告法.
3. **Listing-fee economics, not transaction commission** — moving from 15% commission to a flat per-listing or per-lead fee materially strengthens the defense. (Commercial cost: hurts unit economics.)
4. **No itinerary content from platform** — guides write their own offerings; platform does not edit, curate into packages, or sell "themed routes."

Even with all four, the residual risk in **non-pilot cities** is meaningful because MCT enforcement has historically been functional, not formalist. 🔴

### 3.5 Penalties for unlicensed operation ✅
**旅行社条例 Article 48 / 旅游法 Article 95**: confiscation of illegal gains + fine of **10,000–30,000 RMB** (for unlicensed travel-agency business) and, in serious cases, **30,000–100,000 RMB** and revocation of business license. Foreign-invested entities may also face **市场监管局** penalties separately. Platform officers (法定代表人) can face personal sanction.

---

## 4. Q2 — DOES THE 2020 在线旅游经营服务管理暂行规定 APPLY?

### 4.1 Short answer
**🟢 YES — almost certainly, and independent of the travel-agency licensing question.**

### 4.2 Reasoning
**MCT Order No. 4 (2020-10-01)** ✅ governs "在线旅游经营者" defined as operators conducting tourism business through an internet platform, including **平台经营者** (platform operators), **平台内经营者** (in-platform operators), and **旅游者** users. Even under the most generous "information service only" framing of Ctrip-Guides, the platform itself will be at minimum a **平台经营者** providing matching for tourism-related transactions. The Order applies on its face.

### 4.3 Operative obligations that affect system design
Architect — these are hard requirements regardless of which structural path we choose:

| Provision | Obligation | System-design implication |
|---|---|---|
| Art. 7 🟡 | Real-name verification of tourists and platform-internal operators | KYC at signup; passport for foreign tourists |
| Art. 8 🟡 | Verify guides' 导游证 (guide certificate) and keep records | Credential-verification workflow; archive |
| Art. 13 🟡 | Prohibition on "大数据杀熟" (algorithmic price discrimination against repeat users) | Pricing engine cannot personalize prices by user history |
| Art. 14 🟡 | Mandatory complaint handling channel; response SLA | In-platform complaint module |
| Art. 17 🟡 | Data retention — **transaction & log data retained ≥ 3 years** | Storage architecture, deletion policy must respect this floor |
| Art. 21 🟡 | Cooperation with regulatory inspections | API/export for regulator inquiry |

🔴 All article numbers re-verify against published text — Researcher could not confirm in this session.

### 4.4 Important clarification
MCT Order No. 4 is **not a separate license**. It is a conduct regulation. Compliance with it does **not** substitute for a 旅行社业务经营许可证 if one is required under §3 above.

---

## 5. Q3 — DECISION TREE

```
START: Does our matching activity satisfy 旅行社条例 Art. 2 (招徕 / 组织 / 接待)?
│
├── [YES — as currently drafted]
│   │
│   ├─► Are we willing/able to obtain 旅行社业务经营许可证 (inbound endorsement)?
│   │   │
│   │   ├── YES → PATH A  (see §5.1)
│   │   │        License acquisition: ~6–12 months, ~RMB 200K+ deposit,
│   │   │        Chinese-entity requirements, registered capital ≥ RMB 300K,
│   │   │        qualified manager, fixed premises. ✅ 🟡
│   │   │
│   │   └── NO  → must restructure; go to "NO" branch
│   │
│   └── [Restructure to fall outside Art. 2]
│       │
│       ├─► Operating in 导游自由执业 pilot region for that booking?
│       │
│       ├── YES → PATH B-pilot  (§5.2) — information-service framing viable
│       │
│       └── NO  → PATH C  (§5.3) — must route through licensed agency partner
│
└── [NO — pure information service from day 1]
    │
    └─► PATH B-pure (§5.2) — but only sustainable if
        (i) flat listing fee economics, (ii) no payment custody,
        (iii) no platform-curated itineraries,
        (iv) ToS clearly disclaims operator status.
```

### 5.1 PATH A — Obtain the Travel Agency Permit Ourselves
**Requirements** (旅行社条例 Art. 6–8): ✅ 🟡

- PRC-incorporated entity (the foreign-invested route is now more permissive post-2017 but still requires WFOE/JV setup); 🔴 verify current FIE rules with counsel
- Registered capital ≥ **RMB 300,000** for domestic+inbound; outbound requires more
- Security deposit: **RMB 200,000** (domestic+inbound) — **inbound only +RMB 140,000**, total **RMB 340,000** for our MVP scope 🟡
- Fixed business premises
- Manager with ≥ 3 years tourism-industry experience
- Application to provincial-level 文旅厅; review typically 20 working days
- **Realistic timeline including FIE incorporation: 6–12 months**

**Constraint:** also triggers **导游派遣** rules — once we are a travel agency, the guides become statutorily our dispatched workforce, which **collapses the independent-contractor model** (see §7 below — major commercial and tax implication).

### 5.2 PATH B — Operate as Information Service
**Conditions** (must hold all 4): 🟢→🟡 sliding scale of strictness

1. Service contract is **guide ↔ tourist**; platform is a non-party intermediary.
2. Platform charges a **listing / subscription / lead fee** — NOT % commission on tour value (this is the hardest commercial pivot).
3. Platform does NOT hold payment in custody longer than necessary; ideally, payment flows direct guide↔tourist via PSP with platform billing separately for its fee. 🟡 (note: foreign card → CNY payout architecture makes this hard; see Architect handoff)
4. No platform-curated itineraries, packages, or "themed routes."

**Plus:** for **non-pilot cities** (Beijing, Xi'an, Chengdu likely non-pilot 🔴), even with the four conditions, residual enforcement risk exists because Art. 38 of the Tourism Law historically requires guides to be **dispatched by a travel agency** or to operate through a 导游服务公司. The pilot was the carve-out.

### 5.3 PATH C — Partner with Licensed Travel Agency
The platform operates as a **technology/marketing service provider** to one or more licensed travel agencies. The travel agency is the contracting party with the tourist; the platform invoices the agency for SaaS/marketing/lead-generation fees.

- Pros: clean licensing posture; 文旅 enforcement risk shifts to the partner. 🟢
- Cons: revenue share with partner (industry norm 🟡 5–10% of tour value goes to agency on top of guide fee); slower unit economics; partner concentration risk; partner can fork the platform.
- This is the **fastest path to legal launch** in non-pilot cities.

### 5.4 The "middle path" — Hybrid B-pilot + C
This matches Researcher's recommendation and the PRD v1.2 §0 Path B+C hybrid:

- In **pilot cities**: operate as information service (Path B-pilot), guide contracts direct with tourist.
- In **non-pilot cities** (likely all 4 MVP cities 🔴): route bookings through a licensed partner agency (Path C).
- Single user experience; routing decided server-side by city.

**Caveat**: this hybrid only works if **all four MVP cities** can be cleanly bucketed. Researcher could not confirm 2025–2026 pilot scope. If Shanghai is still in the pilot but Beijing/Xi'an/Chengdu are not, only 25% of bookings get the lighter framework — and we'd be carrying full Path C infrastructure anyway, which argues for simply using Path C universally for v1.

---

## 6. Q4 — THREE ALTERNATIVE BUSINESS STRUCTURES, RATED

| # | Structure | Description | Rating | Rationale |
|---|---|---|---|---|
| **1** | **Travel-Agency-Owned Platform** (Path A) | We obtain our own 旅行社业务经营许可证 with inbound endorsement; guides become contracted suppliers under Tourism Law Art. 38 framework. | 🟢 **GREEN** — fully licensed posture | Slowest (6–12 mo), highest capex, but legally bulletproof. Forces W-2-equivalent treatment of guides → high tax/HR overhead. |
| **2** | **Pilot-City Information Service Only** (Path B-pure, restricted launch) | Launch only in confirmed pilot cities; flat listing-fee economics; no payment custody; no itineraries. | 🟡 **YELLOW** — defensible but novel | Strongest legal narrative, but (a) Beijing/Xi'an/Chengdu likely not in pilot, killing MVP scope, (b) flat-fee model destroys unit economics, (c) "no payment custody" is incompatible with foreign-card → CNY payout flow. |
| **3** | **Licensed-Agency Partner Model** (Path C) | We are a tech/marketing SaaS vendor to 1–3 licensed travel agencies per city; agency is the contracting tour operator; we earn a SaaS+lead fee. | 🟢 **GREEN** (with partner DD) | Fastest path to lawful launch in non-pilot cities. Main risks are commercial (partner concentration) and contractual (partner DPA, brand control, SLA). |
| **4** *(bonus)* | **Hybrid B-pilot + C** | Per-city routing as in §5.4. | 🟡 **YELLOW-GREEN** | Operationally complex; needs verified pilot list; recommend only after counsel confirms 2026 pilot scope. |
| **5** *(bonus)* | **Current model as drafted** (15% commission, payment custody, platform-marketed) | The status quo PRD. | 🔴 **RED** — likely unlicensed travel-agency business | Triggers 旅行社条例 Art. 48 / 旅游法 Art. 95. Do not launch. |

---

## 7. CROSS-CUTTING ISSUES FLAGGED FOR THE TEAM

### 7.1 Guide classification (Architect, HR, Tax)
Tourism Law **Art. 38** and 导游管理办法 historically require a guide to either (a) be employed by, or (b) be **dispatched by**, a travel agency or a 导游服务公司 — **unless** the guide is in the 自由执业 pilot. 🟡

- Under **Path A**: our platform-agency becomes the dispatching agency → guides are unlikely to survive an "independent contractor" classification challenge under PRC labor-and-social-insurance audits. This is a **major** business-model change.
- Under **Path B-pilot**: independent-contractor framing is defensible **in pilot regions only**.
- Under **Path C**: independent-contractor framing depends on the partner-agency contract structure (the partner is the dispatcher; we're a tech vendor — defensible but needs careful contracting).

A separate memo on guide contractor classification will follow once business path is selected.

### 7.2 Payment processing & foreign-card → CNY payout (Architect, Finance)
- Cross-border acquiring requires a PRC **支付业务许可证** OR partnering with a licensed PSP (UnionPay International, Alipay International, etc.). 🟡
- Holding tourist funds in custody for any meaningful duration may also implicate **non-bank payment institution** rules (PBOC 《非银行支付机构条例》, 2024). 🔴 verify.
- The "no payment custody" condition for Path B-pure is hard to reconcile with our PSP architecture. Flag to Architect.

### 7.3 Cross-border data transfer (Privacy DPIA — separate workstream)
Foreign tourists' passport data, payment data, and location data leaving China implicates **PIPL Articles 38, 39, 40** (separate consent, security assessment thresholds, CAC standard contract). Will be addressed in the Privacy Impact Assessment — out of scope here, but signaling that Path A vs B vs C does **not** change PIPL obligations.

### 7.4 Marketing copy (广告法 screen — separate workstream)
Foreign-tourist marketing in English may still be subject to 广告法 when published into Chinese channels or by a Chinese entity. "Best guides in Beijing," "top-rated," "唯一持证" etc. would all trip **Art. 9(3)** absolute-terms prohibition. To be screened separately.

---

## 8. RECOMMENDED NEXT STEPS (in order)

1. **Engage external counsel** — Beijing- or Shanghai-based 文旅 specialist. Top of brief: re-verify §3 Art. 2 enforcement theory; re-verify pilot-city scope for 2026; pressure-test Path C contracting structure.
2. **Researcher** to retry primary-source verification of:
   - Current 导游自由执业 pilot scope (cities/provinces, 2025–2026) 🔴
   - MCT Order No. 4 final article numbering & 2024 amendments (if any) 🔴
   - Recent enforcement actions (2023–2026) against guide-matching platforms 🔴
3. **Architect** to receive a separate handoff brief on which **non-negotiable system requirements** flow from MCT Order No. 4 regardless of business-model path chosen (§4.3 table).
4. **Product/Founder decision**: select Path A, Path B-pilot-only, Path C, or hybrid. **Strong default recommendation: Path C for MVP**, with Path A or hybrid as a 12-month follow-on once volume justifies.
5. **Legal** to draft (a) ToS, (b) Privacy Policy, (c) Guide Contractor Agreement, (d) Partner-Agency MSA — **only after the business-path decision is made**, because the contracts diverge materially.

---

## 9. KEY ASSUMPTIONS & OPEN ITEMS

| # | Assumption | Risk if wrong |
|---|---|---|
| A1 | Beijing, Xi'an, Chengdu are **not** in the 导游自由执业 pilot in 2026; Shanghai status uncertain. 🔴 | If wrong (any of them in pilot), Path B-pilot becomes more attractive. |
| A2 | MCT enforces Art. 2 "组织" verb functionally to capture commission-charging matchmakers. 🟡 | If wrong (formalist reading), Path B-pure becomes safer than rated. |
| A3 | Researcher's recollection of 旅行社条例 Art. 48 penalty range is current. 🔴 | Penalty magnitude affects risk-tolerance calculus. |
| A4 | Inbound endorsement on travel-agency permit still requires +RMB 140K deposit. 🟡 | Affects Path A cost. |
| A5 | "Foreign tourist" status does not by itself elevate guide-matching to outbound-permit territory (it's inbound from PRC perspective). ✅ | Low risk. |
| A6 | No 2024–2026 amendment has materially altered Art. 2 of 旅行社条例. 🔴 | Could change everything. |
| A7 | The platform-operating entity will be PRC-incorporated (or have a PRC subsidiary). | If pure offshore entity serving PRC consumers, **separate** cross-border services + ICP issues arise. Out of scope of this memo. |

---

## 10. FINAL DETERMINATION

> **🟥 DRAFT FOR ATTORNEY REVIEW. NOT LEGAL ADVICE.**
>
> **DO NOT LAUNCH** the platform under the current PRD v1.2 structure (15% commission + payment custody + platform-as-counterparty + non-pilot MVP cities). On the face of 旅行社条例 Article 2 and 旅游法 Article 28, this constitutes unlicensed travel-agency business and exposes the entity and its officers to penalties under 旅行社条例 Article 48 and 旅游法 Article 95.
>
> **RECOMMENDED MVP PATH: Path C (Licensed-Agency Partner Model)** — rated 🟢 GREEN subject to partner due diligence and partner contracting. This is the fastest lawful route to revenue across all four MVP cities.
>
> **OPTIONAL UPGRADE PATH: Path A (own-license)** — rated 🟢 GREEN, 6–12 month timeline, requires major guide-classification rework.
>
> **HIGH-RISK PATH TO AVOID FOR NOW: Path B-pure or status-quo PRD** — rated 🔴 RED / 🟡 YELLOW respectively, until counsel confirms pilot scope and enforcement posture.

— Legal, Ctrip-Guides
*End of memo. Awaiting Researcher re-verification of items A1, A2, A3, A6 and external counsel engagement before any operational reliance.*