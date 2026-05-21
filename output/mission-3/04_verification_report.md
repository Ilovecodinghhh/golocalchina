# Legal Document Completeness Review — Researcher Findings

**To:** Legal
**From:** Researcher
**Date:** 2026-05-21
**Subject:** RE: Verify legal documents completeness
**Methodology note:** Web search tool returned no results for the two queries attempted this session. Findings below are drawn from my training-data knowledge of publicly-available competitor ToS (Klook, GetYourGuide, Viator/Tripadvisor, Trip.com), PIPL/CSL/DSL statutory text, and CAC/MIIT enforcement bulletins through ~early 2025. **All items below should be cross-checked against the live versions of competitor documents before publication** — competitor ToS change frequently. I have flagged confidence levels throughout.

---

## ⚠️ Top-level caveat

Because live web verification failed this session, I cannot quote current clause numbers from Klook/GYG/Viator ToS. Treat this as a **gap-hypothesis list** to validate, not a definitive audit. I recommend Legal commission a paid Westlaw/LexisNexis or Chinese 北大法宝 search for the China enforcement question (item 4) before relying on the answer.

---

## 1) GAPS vs. Klook / GetYourGuide / Viator ToS

### 🔴 LIKELY GAPS (high confidence these competitors include them; verify ours does)

| # | Clause | Why it matters | Source/precedent |
|---|---|---|---|
| 1.1 | **UGC license grant from user → platform** (reviews, photos, tour notes) — perpetual, royalty-free, sublicensable, worldwide | Without it you can't legally display tourist reviews/photos in marketing | Standard across Klook §10, GYG §11, Viator §9 *(clause numbers from memory — verify)* |
| 1.2 | **Liability cap stated as a hard number** (e.g., "greater of booking value or USD 100") | "Information platform" disclaimer alone is not a substitute for a cap; PRC courts have upheld reasonable caps if conspicuous | Viator caps at booking value; GYG at €100 |
| 1.3 | **Class action waiver / mass arbitration carve-out** | Critical if US tourists sue; you'll be in CIETAC or HK arbitration but US plaintiffs' bar still tries | Viator §16 (US users) |
| 1.4 | **Mandatory pre-suit notice + 30-day cure period** | Cheap defense against impulse litigation | GYG §17 |
| 1.5 | **Sanctions / restricted-jurisdiction clause** (OFAC, EU sanctions list, China MoFCOM unreliable entity list) | You will get bookings from Iranian/Russian/N. Korean tourists; need contractual basis to refuse | All three competitors have this |
| 1.6 | **Apple App Store / Google Play pass-through terms** (if you ship a mobile app) | Apple §3.2 of Developer Agreement *requires* certain EULA passthroughs | Standard Apple boilerplate |
| 1.7 | **Currency conversion / FX disclaimer** | Tourists will be charged in CNY but see USD/EUR estimates — you need a "estimate only" clause | Klook explicitly |
| 1.8 | **Promo code / voucher T&Cs** (no cash value, expiry, anti-stacking, anti-fraud forfeiture) | Even if MVP doesn't have promos, draft it now so Growth team can launch without a legal sprint | Klook §13 |
| 1.9 | **Account-suspension grounds enumerated specifically** (not just "at our discretion") | PRC consumer protection law (《消费者权益保护法》Art. 26) disfavors purely-discretionary unilateral termination | — |
| 1.10 | **Tourist age requirement (18+) and minor accompaniment rules** | Liability magnet otherwise; book-on-behalf-of-minor provisions needed | GYG §3 |
| 1.11 | **Beta/experimental feature disclaimer** | For when you launch AI itinerary builder, etc. | Common boilerplate |
| 1.12 | **No-show / late-arrival policy** | Tourism-specific; tourists missing pickup is the #1 dispute on Klook per their help center | Klook help center |

### 🟢 LIKELY CONFIRMED (your draft already addresses, based on the preamble)

- ✅ Platform-role notice ("not a travel agency, not a tour operator") — your preamble nails this; this is your single most important clause and it is **stronger and clearer** than Klook's equivalent language
- ✅ Bilingual document with controlling-language clause flagged for counsel
- ✅ Independent-contractor framing of guides
- ✅ "Not party to the service contract" — defensive posture

---

## 2) GAPS vs. PIPL-compliant Privacy Policies

### 🔴 LIKELY GAPS

| # | Clause | PIPL/GDPR basis | Notes |
|---|---|---|---|
| 2.1 | **Named list of overseas recipients** (entity name, contact, country, purpose, categories of PI) | **PIPL Art. 39** — mandatory before any cross-border transfer | Must be a *table*, not prose. Includes Airwallex (HK/SG), and any non-PRC tourist destination data export |
| 2.2 | **Cross-border transfer mechanism selected** — Standard Contract (个人信息出境标准合同) / Security Assessment / Certification | PIPL Art. 38; CAC Standard Contract Provisions (2023.06.01 effective) | If foreign tourist data flows back to their home country (e.g., via email receipts), this triggers. Note: **CAC issued 《促进和规范数据跨境流动规定》(March 2024)** which *relaxed* thresholds — only >100k non-sensitive PI or >10k sensitive PI annually triggers Standard Contract. Worth referencing. |
| 2.3 | **Separate consent (单独同意) for each sensitive PI category** | PIPL Art. 29 | Sensitive PI here likely includes: passport number, biometric (if face liveness used), location traces during tours, payment card. Each needs its own consent action, not bundled |
| 2.4 | **Automated decision-making opt-out + non-discriminatory pricing pledge** | PIPL Art. 24 (no 大数据杀熟 / algorithmic price discrimination); 《互联网信息服务算法推荐管理规定》(2022) | Required if you ever do dynamic pricing, guide-ranking algorithm, or personalized recommendations. Recommend drafting now |
| 2.5 | **Algorithm filing reference / 算法备案编号** placeholder | 算法推荐管理规定 Art. 24 | If you operate any recommendation algorithm, you must file with CAC and disclose the filing number in-product |
| 2.6 | **Deceased user data — close relatives' rights** | PIPL Art. 49 | Often forgotten. Pre-drafted clause is cheap insurance |
| 2.7 | **Children under 14 — guardian consent + separate children's rules** | PIPL Art. 31; 《个人信息保护法》+《未成年人保护法》 + GB/T 41391 *Children's PI Protection Specification* | Tourists travel with kids. Even if you ban <18 accounts, you'll process children's photos in family tours |
| 2.8 | **PIPIA (Personal Information Protection Impact Assessment) commitment** | PIPL Art. 55 — mandatory for sensitive PI processing, cross-border, automated decisions | Cite that you've conducted it |
| 2.9 | **Breach notification SLA** — to user *and* to CAC | PIPL Art. 57 (notify both); typical SLA 72h to regulator | GDPR Art. 33 also 72h |
| 2.10 | **DPO / 个人信息保护负责人 contact** | PIPL Art. 52 — mandatory once you process >1M users' PI | Plan ahead. Name and email required |
| 2.11 | **Data subject rights mechanism** — *how* to exercise (in-product flow, email, response SLA — PIPL says 15 working days) | PIPL Arts. 44–47, 50 | Often vague in drafts; needs concrete process |
| 2.12 | **Cookies & SDK list table** | 《App违法违规收集使用个人信息行为认定方法》(MIIT/CAC 2019) + GDPR ePrivacy parallel | Must list every embedded SDK with vendor, purpose, data collected. **This is the #1 trigger for MIIT app-takedown sweeps.** |

### 🟢 LIKELY CONFIRMED

- ✅ Dual PIPL+GDPR framing
- ✅ Controller/processor mapping (Airwallex independent; Tencent IM/MT, Amap entrusted)
- ✅ Counsel-review flags on jurisdictional assumptions

---

## 3) Third-Party Service Coverage Check (per tech spec)

| Service | Role | Covered in current draft? | Action |
|---|---|---|---|
| **Airwallex** | Payment / card data | ✅ Yes — flagged as independent controller | Confirm contractual posture (joint vs. C2C); add to Art. 39 overseas-recipient table (Airwallex is HK-domiciled) |
| **Tencent IM (即时通信)** | In-app chat | ✅ Yes — entrusted processor | Add SDK details to cookies/SDK table (item 2.12). Confirm Tencent's standard DPA is signed |
| **Tencent Machine Translation (腾讯翻译君)** | Chat translation | ✅ Yes — entrusted processor | ⚠️ **Flag:** translation API sends tourist messages to Tencent. If messages contain sensitive PI (medical conditions, dietary, location), need explicit consent for translation purpose |
| **Amap (高德地图)** | Location / mapping | ✅ Yes — entrusted processor | ⚠️ Location is sensitive PI under PIPL — needs separate consent (item 2.3) |
| **Aliyun (阿里云)** | Cloud hosting | ⚠️ **Partial — mentioned as hosting only.** Should be explicitly named as infrastructure processor with DPA reference | **GAP** |

### 🔴 Likely uncovered third parties (verify against tech spec)

Has Legal confirmed with Engineering whether the stack also includes any of:

- **Identity verification vendor** (face liveness, passport OCR) — e.g., 旷视/Megvii, 商汤/SenseTime, Aliyun RealPerson — collects **biometric** sensitive PI, requires explicit separate consent
- **SMS gateway** (Aliyun SMS, Tencent Cloud SMS, or international: Twilio/Vonage for foreign tourist phone verification) — Twilio/Vonage = cross-border transfer of phone numbers
- **Email service** (SendGrid, Aliyun DirectMail) — same cross-border concern if international vendor
- **Push notifications** (Tencent TPNS/Jiguang/Getui/APNs/FCM) — APNs/FCM = cross-border to Apple/Google
- **Crash reporting** (Bugly/Sentry/Firebase Crashlytics)
- **Analytics** (Aliyun Quick BI, Sensors Analytics 神策, GA4)
- **CAPTCHA** (NetEase 易盾, Tencent 防水墙, Geetee 极验, hCaptcha, reCAPTCHA)
- **Customer support** (Zendesk, Intercom — both cross-border; or domestic 美洽/小能)
- **Public security ID validation** (公安部 居民身份证联网核查 — for guide 导游证 verification, this hits 文旅部's 全国导游公共服务监管平台 API)

**Recommendation:** Request engineering's full SDK/SaaS bill-of-materials before publishing the Privacy Policy.

---

## 4) GAPS in Guide Agreement (independent-contractor + tourism standards)

### 🔴 LIKELY GAPS — Standard tourism-platform contractor clauses

| # | Clause | Rationale |
|---|---|---|
| 4.1 | **Background check authorization + criminal-record disclosure** | Tourists' physical safety. Klook's "Klook Quality" program and GYG's Originals program both require this |
| 4.2 | **Mandatory professional liability insurance (责任险) + minimum coverage** | Some Chinese provinces (e.g., Beijing, Shanghai) require licensed guides to carry insurance; even where not required, contractually required is standard |
| 4.3 | **导游证 verification cadence** — guide must consent to platform re-verifying via 全国导游公共服务监管平台 / 电子导游证 system at any time; auto-suspension if 导游证 expires/revoked | Critical for ongoing compliance. The 电子导游证 (electronic guide card) under 文旅部's 2017 reform makes real-time verification feasible |
| 4.4 | **Non-circumvention clause** — guide may not solicit platform tourists off-platform for 24 months post-tour | Marketplace economics. **But** balance against IC status defense (too restrictive = looks like employment); 12–24 months and limited to *specific tourists matched via platform* is the sweet spot |
| 4.5 | **No subcontracting / no substitute guide without platform approval** | Both IC-defense (control over *whom*, not *how*) and tourist safety. Wait — review carefully: in California-style IC tests, "right to substitute" actually *helps* IC status. In China, 事实劳动关系 test focuses more on integration, payment regularity, exclusivity. Recommend allowing substitution *with platform notification* |
| 4.6 | **Anti-bribery / anti-kickback** (no commissions from shops/restaurants without disclosure) | This is the *single biggest* reputational risk in China inbound tourism — "强制购物" 强制购物 (forced shopping) scandals. Beijing/Yunnan/Hainan have all had high-profile cases. Strong clause needed |
| 4.7 | **Code of conduct** — anti-harassment, anti-discrimination (especially on nationality/religion given foreign-tourist user base), dress code, language standards |
| 4.8 | **Emergency response duties** — call 110/120/119; notify platform within X hours; cooperate with embassy notifications |
| 4.9 | **Tax responsibility** — guide is responsible for own individual income tax (个人所得税) on "labor remuneration" (劳务报酬所得); platform withholds per 国家税务总局 rules where required | Don't conflate with employment-wages withholding |
| 4.10 | **Platform IP license** — limited, revocable license to use Ctrip-Guides brand/logo only in connection with platform-matched tours; no use in off-platform marketing |
| 4.11 | **Guide content license to platform** — perpetual, royalty-free, worldwide license to display guide's bio, photos, tour descriptions, sample itineraries on platform; survives termination *for content posted during term* |
| 4.12 | **Tourist personal information confidentiality** — guide is a *separate* PI processor under PIPL for tourist data received; bound by separate DPA terms |
| 4.13 | **Right to recover overpayments / refund clawback** — if tourist successfully chargebacks, platform can offset against future guide payouts |
| 4.14 | **Survival clauses** — confidentiality, IP licenses, indemnity, non-circumvention, tax must survive termination |
| 4.15 | **Audit rights** — platform may audit guide's compliance (insurance, 导游证, tax filings) on reasonable notice |
| 4.16 | **Cooperation in tourist disputes / arbitration** — guide must participate in dispute resolution |

### 🔴 IP protection — bilateral check

**Platform → Guide direction (likely covered):**
- ✅ Trademark / brand license (limited)
- ✅ Platform software/IP retained

**Guide → Platform direction (verify these are present):**
- Likeness rights: guide's name, face, voice used in marketing — needs explicit consent + termination handling
- Tour content / itineraries authored by guide — platform license vs. ownership
- Tour photos taken by guide during tours featuring tourists — overlap with tourist privacy
- AI-generated content from guide's prompts (if you launch AI tour-builder) — ownership allocation
- Reviews of tourists by guide (if you have two-sided reviews) — UGC license
- Trade secret: guide's proprietary itineraries/routes — does guide retain? Recommend guide *retains* (helps IC status) but grants license

**⚠️ Specific recommendation:** Add a clause that **upon termination, platform may continue displaying historical reviews/booking history for transparency, but must remove guide's bio/photos/active listings within X days** — this addresses GDPR right-to-erasure for EU tourists who might be guides too.

---

## 5) Tourist Safety / Emergency — ToS adequacy

Based on the preamble snippet, your ToS positions you as pure information platform, which is correct for liability. But you still need affirmative tourist-protection clauses to:
1. Pass MCT (文旅部) and consumer-protection scrutiny
2. Avoid the "platform did nothing" optics in a high-profile incident

### 🔴 GAPS to add to ToS

- **24/7 emergency hotline / in-app SOS** commitment — even if you just escalate to 110/120, document the SLA
- **Embassy / consulate notification commitment** for foreign tourist death or serious injury (some embassies expect this proactively)
- **Travel advisory display** — restricted regions (Tibet TAR requires permits; border zones; certain Xinjiang prefectures have de facto restrictions for foreign tourists)
- **Force majeure protocol** specific to: typhoons (Hainan, Fujian, Guangdong), earthquakes (Sichuan, Yunnan, Tibet), sandstorms (Inner Mongolia, Gansu), heavy snow, COVID-era public health measures
- **Lost passport / lost item assistance** — describe the platform's role (typically: refer to nearest 公安出入境)
- **Medical pre-disclosure** prompt — tourist self-discloses allergies/conditions to guide pre-tour (data minimization: store on tourist side, share to guide for that booking only)
- **Solo female traveler protections** (optional but increasingly expected) — female guide opt-in, code-of-conduct enforcement
- **Anti-forced-shopping pledge** with reporting mechanism — directly addresses the highest-profile China inbound tourism scandal pattern (see 4.6)
- **Insurance recommendation** — strongly recommend tourist purchase travel insurance; clarify platform does not insure

---

## 6) Recent Enforcement Actions (2024–2026)

⚠️ **Confidence: LOW** — web search failed, and my training data is sparse on 2025–2026 specifics. **Strong recommendation: human verification via 北大法宝 / Westlaw China / CAC.gov.cn news section.**

### What I can say from training data (verify before citing):

- **CAC quarterly app-takedown bulletins** — CAC and MIIT continue periodic sweeps. MIIT 《关于侵害用户权益行为的App通报》is published roughly quarterly; common violations are: excessive permission requests, opaque SDK lists, deficient privacy policies, no opt-out for personalized recommendations
- **PIPL Standard Contract enforcement** — CAC began accepting Standard Contract filings from June 2023; by 2024 multiple platforms had filings rejected for inadequate PIPIAs
- **March 2024 — 《促进和规范数据跨境流动规定》** — relaxed cross-border thresholds; if your draft was written against pre-March-2024 rules, the thresholds may be out of date
- **Didi precedent** (¥8.026B fine, July 2022) — still the lodestar for CSL/DSL/PIPL stacking penalties; mention in PIPIA as a referenced risk
- **2024 — multiple OTAs reportedly under CAC inspection** for cross-border data and SDK disclosure issues; **I cannot confirm specific named platforms without verification**
- **Cultural & Tourism Ministry 文旅部 enforcement** — annual "不合理低价游" (unreasonably low-price tour) sweeps, with platform liability under 《旅游法》Art. 35. Your "information platform" positioning helps but doesn't eliminate this — if a guide on your platform sells a tour at unreasonably low prices with forced shopping, you can be implicated as a 提供者 (provider)

### 🔴 SPECIFIC RECOMMENDATION

Add a clause-cluster in ToS:
- Platform monitors for and may suspend listings priced suspiciously low ("indicia of 不合理低价游")
- Platform prohibits and will sanction forced shopping
- Platform reserves right to cooperate with 文旅部 / 公安 inspections

---

## SUMMARY TABLE

| # | Question | Result |
|---|---|---|
| 1 | Klook/GYG/Viator ToS gaps | **12 likely gaps identified** (1.1–1.12); UGC license, liability cap, class waiver, sanctions clause are highest priority |
| 2 | PIPL Privacy Policy gaps | **12 likely gaps identified** (2.1–2.12); Art. 39 overseas-recipient table, separate consents for sensitive PI, SDK list, and DPO contact are highest priority |
| 3 | Guide agreement gaps | **16 likely gaps identified** (4.1–4.16); 导游证 re-verification, anti-forced-shopping, insurance, non-circumvention scope are highest priority |
| 4 | 2024–2026 enforcement | ⚠️ **Cannot confirm specific cases**; general trend = SDK disclosure + cross-border + 算法推荐 are top CAC targets. **Needs paid-database verification.** |
| Safety/emergency | **8 ToS clauses to add** (24/7 hotline, embassy notification, force majeure, anti-forced-shopping pledge) |
| 3rd-party coverage | **Aliyun partial; ID verification, SMS, push, analytics likely missing** — request full BoM from Engineering |
| Guide IP bilateral | **Guide→Platform direction underspecified** — likeness, content license, post-termination removal SLA needed |

---

## CONFIRMED (your draft is solid on)

1. ✅ **Path-B positioning** — "information service platform, not travel agency" is the right architecture and is articulated more clearly than Klook's equivalent
2. ✅ **IC-status defense architecture** — Schedule A approach (factor-by-factor) is best practice
3. ✅ **Dual PIPL + GDPR framing** for Privacy Policy
4. ✅ **Controller/processor mapping** — Airwallex as independent controller, Tencent/Amap as entrusted processors is the correct posture
5. ✅ **Bilingual + controlling-language flagging** for counsel
6. ✅ **Counsel-review markers** throughout — exactly the right discipline for a 0.1 draft

---

## NEXT STEPS I RECOMMEND

1. **Architect / Engineering:** Request full SDK + third-party SaaS bill-of-materials for Privacy Policy SDK table
2. **Legal:** Commission paid-database search (北大法宝, Westlaw China) for 2024–2026 CAC/MIIT enforcement against tourism platforms specifically
3. **Researcher (me):** Once web search is restored, I can pull live Klook / GYG / Viator ToS for line-by-line gap analysis — let me know if you want this prioritized
4. **Legal:** Draft the missing clause-clusters in order of regulatory risk: (a) PIPL Art. 39 table, (b) SDK list, (c) anti-forced-shopping cluster, (d) UGC license, (e) liability cap

— Researcher