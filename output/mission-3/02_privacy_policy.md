# Privacy Policy — Ctrip-Guides Platform

**Document type:** ⚠️ **DRAFT FOR ATTORNEY REVIEW — NOT FINAL LEGAL ADVICE**
**Version:** 0.1 (Dual PIPL + GDPR compliance)
**Prepared by:** Legal (in-house draft)
**Date:** 2026-05-21
**Effective date:** [TBD — must not be earlier than the date this policy is published in-app and consent is re-collected from existing users]

---

## ⚠️ Drafting Notes for Counsel (delete before publication)

1. **Jurisdiction assumptions made in this draft:**
   - Platform operating entity is a PRC-incorporated company (the "Operator"); data processing infrastructure is primarily hosted on PRC cloud (Tencent Cloud / Alibaba Cloud) inside mainland China. [COUNSEL REVIEW: confirm entity structure and hosting topology — if any production data sits outside the PRC, the cross-border transfer analysis flips.]
   - The Operator is the **personal information handler (个人信息处理者)** under PIPL Art. 73(1) and the **controller** under GDPR Art. 4(7) for the data described herein.
   - Airwallex is treated as an **independent controller / independent personal information handler** for card data (it is a licensed PSP that determines its own purposes and means for payment processing). [COUNSEL REVIEW: confirm contractual posture with Airwallex — joint controllership vs. controller-to-controller.]
   - Tencent IM (chat), Tencent Machine Translation, and Amap are treated as **entrusted processors / 受托人** under PIPL Art. 21 and **processors** under GDPR Art. 28. [COUNSEL REVIEW: confirm DPAs are in place; verify each vendor's actual role.]
2. **Languages:** This English version is the working draft. A 中文版 will be issued; for PRC users the Chinese version controls; for non-PRC users [COUNSEL REVIEW: which controls].
3. **PIPL "Responsible Person" (个人信息保护负责人):** required under PIPL Art. 52 once processing volume thresholds are met. Threshold is set by CAC at 1 million individuals (per 《个人信息保护合规审计管理办法》 and related guidance). We are likely to cross this threshold within Year 1 — appointing one from day one is conservative best practice. [COUNSEL REVIEW]
4. **GDPR EU representative (Art. 27):** required because the Operator is established outside the EU but offers services to EU data subjects. A representative must be appointed in an EU Member State. [COUNSEL REVIEW: representative not yet appointed — block on launch in EU markets until done.]
5. **Cross-border transfer mechanism (PIPL Art. 38):** this draft assumes we will rely on **CAC Standard Contract (标准合同) filing** under 《个人信息出境标准合同办法》(March 2023) for transfers to EU tourists' home countries, NOT security assessment (we are below the threshold) and NOT certification. [COUNSEL REVIEW: re-evaluate when annual transfer volume approaches 100,000 individuals or sensitive PI of 10,000 individuals — would push us into mandatory CAC security assessment.]

---

## 1. Introduction / 引言

Ctrip-Guides (the "Platform", "we", "us", "our") is operated by [Operator legal name 运营主体] ("Operator"), a company incorporated in the People's Republic of China with registered address at [address] and unified social credit code [USCC].

This Privacy Policy explains how we collect, use, store, share, transfer, disclose, and otherwise process personal information ("PI" / 个人信息) of tourists ("Tourists") and licensed tour guides ("Guides") (collectively, "Users") when you use our website, mobile application, or related services (the "Services").

This policy is designed to comply with:

- **The Personal Information Protection Law of the PRC (《中华人民共和国个人信息保护法》, "PIPL")** — applicable to all Users whose PI is processed in connection with the Services.
- **The EU General Data Protection Regulation (Regulation (EU) 2016/679, "GDPR")** — applicable to Tourists located in the European Economic Area ("EEA") at the time of using the Services, and to processing of their data after they return home.
- **The PRC Cybersecurity Law (《网络安全法》) and Data Security Law (《数据安全法》)** to the extent applicable.

Where PIPL and GDPR impose different obligations, **we apply the stricter standard** to all Users. Sections labelled "[GDPR only]" apply only to EEA-resident Tourists.

---

## 2. Definitions / 定义

- **Personal Information / 个人信息 (PI):** any information, recorded electronically or otherwise, relating to an identified or identifiable natural person, excluding anonymized information (PIPL Art. 4; GDPR Art. 4(1)).
- **Sensitive Personal Information / 敏感个人信息:** PI that, if leaked or misused, is liable to result in infringement of personal dignity or harm to personal or property safety, including biometric data, religious beliefs, specific identity, medical/health data, financial accounts, location tracking, and PI of minors under 14 (PIPL Art. 28). Under GDPR, "special category" data per Art. 9.
- **Processing / 处理:** collection, storage, use, refinement, transmission, provision, disclosure, deletion, etc. (PIPL Art. 4; GDPR Art. 4(2)).
- **Personal Information Handler / 个人信息处理者 ("Handler"):** the Operator, equivalent to "controller" under GDPR Art. 4(7).
- **Entrusted Party / 受托人:** a third party processing PI on our behalf under our instructions, equivalent to "processor" under GDPR Art. 4(8).

---

## 3. What Personal Information We Collect / 我们收集的个人信息

### 3.1 Tourist data

| Category | Specific data | Source |
|---|---|---|
| Account | Name, email, phone, country of residence, preferred language, preferred currency | You |
| Booking | Guide selected, service dates, service type, total amount | You + Platform |
| Payment | **Card details are held by Airwallex, not by us.** We receive only: transaction ID, last 4 digits, card brand, transaction status, amount | Airwallex |
| Communication | In-app chat messages (auto-translated via Tencent MT), support tickets | You + Guide |
| Location | **City-level only** (derived from booking + IP geolocation). GPS-precise location is collected **only** if you opt in to "Meeting-Point Sharing" on the day of the tour | You / IP-based |
| Reviews | Star rating (1-5), text content | You |
| Device & technical | IP address, browser type, device model, OS, language settings, app version, crash logs | Automatic |

### 3.2 Guide data

| Category | Specific data | Source |
|---|---|---|
| Account | Name, email, phone, city of practice, languages spoken, specialties | You |
| **Credential (sensitive PI)** | 导游证 number, issuing authority, photo of license | You |
| Availability & pricing | Calendar data, hourly/daily rates | You |
| **Payment (sensitive PI)** | Bank account, Alipay ID, or WeChat Pay ID for payout | You |
| Reviews | Star rating, text content received from Tourists | Tourists |
| Earnings | Transaction history, payout records, tax-relevant records | Platform |

### 3.3 Sensitive PI handled (PIPL Art. 28; GDPR Art. 9 where applicable)

- **Guide credential photo** — contains image of person + ID-style document. We obtain **separate consent (单独同意, PIPL Art. 29)** before collection and explain the necessity, purpose, and impact.
- **Guide financial account information** — separate consent collected.
- **Tourist precise location** (only if opted-in) — separate consent collected at the point of activation, with one-tap revocation.
- We do **not** intentionally collect special-category data under GDPR Art. 9 (race, religion, health, sexual orientation, political opinions, trade union membership, biometric data for unique identification). If a User voluntarily discloses such data in chat or reviews, we treat it as inadvertently collected and apply the heightened protections of GDPR Art. 9(2)(e) (manifestly made public) or seek explicit consent.

---

## 4. Purposes and Lawful Bases for Processing / 处理目的与合法性基础

Per PIPL Art. 13 and GDPR Art. 6, every processing activity must rest on a specified lawful basis. The table below maps each purpose to its basis under both regimes.

| # | Purpose | Data used | PIPL lawful basis (Art. 13) | GDPR lawful basis (Art. 6) |
|---|---|---|---|---|
| 1 | Account creation and authentication | Account data | Art. 13(1)(2) — necessary for performance of contract you are a party to | Art. 6(1)(b) — performance of contract |
| 2 | Matching Tourist with Guide (search, filter, booking) | Account, booking, availability | Art. 13(1)(2) — contract | Art. 6(1)(b) — contract |
| 3 | Facilitating payment (handing off to Airwallex) | Payment metadata | Art. 13(1)(2) — contract | Art. 6(1)(b) — contract |
| 4 | In-app chat and auto-translation | Chat messages | Art. 13(1)(2) — contract + Art. 13(1)(1) **consent** for cross-border translation processing | Art. 6(1)(b) + Art. 6(1)(a) consent for translation by Tencent MT |
| 5 | Guide credential verification | Credential data | Art. 13(1)(2) + Art. 29 **separate consent** (sensitive PI) | Art. 6(1)(c) — legal obligation (verifying licensed-guide status under 《导游管理办法》) + Art. 9(2)(g) substantial public interest [COUNSEL REVIEW] |
| 6 | Reviews & ratings publication | Review content, masked name | Art. 13(1)(2) — contract; Art. 1027 PRC Civil Code interest balancing | Art. 6(1)(f) — legitimate interest (LIA documented separately) |
| 7 | Fraud prevention, security, anti-abuse | Device, IP, transaction patterns | Art. 13(1)(3) — statutory duty under Cybersecurity Law Art. 21 | Art. 6(1)(f) — legitimate interest |
| 8 | Tax and accounting recordkeeping | Earnings, transactions | Art. 13(1)(3) — statutory duty (《税收征收管理法》) | Art. 6(1)(c) — legal obligation |
| 9 | Marketing emails / push notifications | Account + behavioral | Art. 13(1)(1) **consent** (opt-in) | Art. 6(1)(a) **consent** (opt-in) per ePrivacy Directive |
| 10 | Service improvement & analytics (aggregated) | Device, usage logs | Art. 13(1)(1) consent for non-essential analytics; legitimate operation for essential | Art. 6(1)(f) for essential analytics; Art. 6(1)(a) for non-essential |
| 11 | Responding to legal requests / court orders | As required | Art. 13(1)(3) | Art. 6(1)(c) |

**We do not use your PI for automated decision-making with legal or similarly significant effects (PIPL Art. 24; GDPR Art. 22)** beyond fraud-scoring of transactions. You have the right to request human review of any fraud-related block (see §9).

---

## 5. How We Share PI with Third Parties / 第三方共享

### 5.1 Service providers (Entrusted Parties / Processors)

We share PI with the following on a need-to-know basis, under written data processing agreements that meet PIPL Art. 21 and GDPR Art. 28:

| Recipient | Role | Data shared | Location | Purpose |
|---|---|---|---|---|
| **Tencent Cloud / Alibaba Cloud** | Entrusted hosting | All categories (encrypted at rest) | Mainland China | Infrastructure |
| **Tencent IM (即时通信 IM)** | Entrusted processor | Chat messages, account ID | Mainland China | Messaging delivery |
| **Tencent Machine Translation (机器翻译)** | Entrusted processor | Chat message text only | Mainland China | Auto-translation |
| **Amap (高德地图)** | Entrusted processor | City name + (if opted in) meeting-point coordinates | Mainland China | Map display, navigation |
| **Airwallex** | **Independent controller / handler** [COUNSEL REVIEW] | Card data, transaction data | Hong Kong / global | Payment processing under its PSP licenses |
| **SMS/email providers** | Entrusted | Phone, email + message content | Mainland China | OTP, notifications |
| **Fraud-detection vendor** | Entrusted | Device/IP/transaction metadata | [COUNSEL REVIEW: confirm vendor + location] | Anti-fraud |

### 5.2 Provision to other Users (PIPL Art. 23 / GDPR controller-to-controller)

- **Tourist → Guide:** at booking confirmation, we share with the matched Guide: Tourist first name, masked phone (last 4), preferred language, meeting-point preferences. The Guide is an **independent handler / controller** of this data thereafter and must comply with PIPL on its own behalf (see Guide Terms §[X]).
- **Guide → Tourist:** we display Guide's professional profile, name, photo, verified credential indicator (✓ verified — we do **not** display the 导游证 number itself), languages, specialties, reviews, and pricing.
- **PIPL Art. 23 disclosure** to the providing User: at the point of provision we inform the providing User of the recipient's name, contact, purpose, and method, and obtain **separate consent**.

### 5.3 Government, regulators, courts

We disclose PI to PRC authorities (including Ministry of Public Security, Ministry of Culture & Tourism, tax authorities, CAC) and EEA authorities where compelled by valid legal process. We push back on overbroad requests and, where lawfully permitted, notify the affected User.

### 5.4 Business transfers

In a merger, acquisition, or asset sale, PI may transfer to the successor entity. We will notify Users (PIPL Art. 22; GDPR Recital 155) and require the successor to honor this Policy or seek fresh consent for material changes.

### 5.5 We do NOT sell your PI to advertisers or data brokers.

---

## 6. Cross-Border Data Transfers / 个人信息出境

### 6.1 PIPL-side transfers (data leaving mainland China)

Per PIPL Art. 38–39, we transfer PI outside mainland China only when one of the following mechanisms is in place:

- **CAC Standard Contract (标准合同)** filed with the provincial CAC under 《个人信息出境标准合同办法》(effective June 2023). This is our primary mechanism. [COUNSEL REVIEW: confirm filing complete prior to launch.]
- **CAC security assessment (安全评估)** — required if we exceed thresholds (cumulative export of non-sensitive PI of 1,000,000+ individuals; sensitive PI of 10,000+ individuals; or we are designated a Critical Information Infrastructure Operator). We are below these thresholds; we will reassess quarterly.
- **Certification (认证)** under 《个人信息保护认证实施规则》 — not currently used.

**Before any cross-border transfer, we provide PIPL Art. 39 notice** (name of overseas recipient, contact, purpose, method, categories of PI, how the User can exercise rights against the overseas recipient) and obtain **separate consent (单独同意)**.

Outbound transfers in scope:
- Tourist account & booking data → mirrored to recipient country for the Tourist's own access when traveling home [COUNSEL REVIEW: confirm whether we actually mirror or only stream on access].
- Tourist data → Airwallex (Hong Kong + global processing for card networks).
- Tourist data → EU representative (for GDPR rights requests from EEA Tourists).

### 6.2 GDPR-side transfers (data entering / processed in China)

For EEA Tourists, processing their PI in mainland China is a transfer outside the EEA under GDPR Ch. V. Because the European Commission has **not** issued an adequacy decision for mainland China, we rely on:

- **EU Standard Contractual Clauses (SCCs)** — Commission Implementing Decision (EU) 2021/914, Module 1 (controller-to-controller) between the EEA Tourist's data flowing to Operator. [COUNSEL REVIEW: SCC module choice — Module 1 if Operator is treated as controller, Module 2 if processor relationship for any sub-flows.]
- **Transfer Impact Assessment (TIA)** completed and on file, addressing PRC government access (post-Schrems II). Supplementary measures include encryption in transit and at rest, minimization, and a policy of pushing back on overbroad PRC authority requests where lawful. [COUNSEL REVIEW: TIA is the highest-risk artefact in this stack — must be prepared and signed off before EU launch.]

EEA Tourists can request a copy of the SCCs and a summary of the TIA at [privacy@ctrip-guides.example].

---

## 7. Data Retention / 数据保留期

We retain PI only as long as necessary for the purposes stated, or as required by law. After the retention period, we delete or anonymize the data (PIPL Art. 47; GDPR Art. 5(1)(e)).

| Category | Retention period | Legal basis for retention |
|---|---|---|
| Account data (active user) | Duration of account + 3 years after closure | Contract, dispute, statute of limitations |
| Account data (inactive — no login 24 months) | Account marked dormant; deletion notice + 30 days then deleted unless user reactivates | PIPL Art. 47(1) — purpose achieved |
| Booking and transaction records | **10 years** from transaction date | 《会计档案管理办法》 Art. 14 (10-year retention for financial records); 《电子商务法》Art. 31 (≥3 years for e-commerce records) |
| Payment metadata (we hold) | 10 years | Same as above |
| Chat messages | 18 months from last message in thread | E-commerce evidentiary needs + 《网络交易监督管理办法》; balanced against minimization |
| Reviews | Until account deletion or User-initiated takedown, plus 90-day rollback window |  |
| Guide credential photo | Duration of guide active status + 5 years | Liability defense; verification audit trail [COUNSEL REVIEW — consider reducing to 2 years post-deactivation] |
| Device/IP logs | 6 months | Cybersecurity Law Art. 21 (≥6 months) |
| Marketing consent records | Until withdrawn + 3 years | Proof of consent |
| Tourist precise location (if opted in) | **24 hours after tour ends, then auto-deleted** | Minimization |

---

## 8. Data Subject / Personal Information Subject Rights / 用户权利

You have the following rights, exercisable free of charge (PIPL Ch. 4; GDPR Ch. 3). We will respond within **15 working days** (PIPL practice) / **30 days** (GDPR Art. 12(3)) — whichever is shorter applies to you.

| Right | Scope | How to exercise |
|---|---|---|
| **Access / 查阅** (PIPL Art. 45; GDPR Art. 15) | Confirm whether we process your PI; obtain a copy | In-app: Settings → Privacy → Download my data |
| **Correction / 更正** (PIPL Art. 46; GDPR Art. 16) | Fix inaccurate PI | In-app self-edit; email for non-editable fields |
| **Deletion / 删除** (PIPL Art. 47; GDPR Art. 17) | Request deletion when purpose achieved, consent withdrawn, etc. | In-app: Settings → Delete account |
| **Restriction / 限制处理** (GDPR Art. 18) [GDPR only] | Pause processing in defined circumstances | Email |
| **Portability / 可携带** (PIPL Art. 45 para. 3; GDPR Art. 20) | Receive your PI in a structured, machine-readable format and have it transmitted to another handler where technically feasible | In-app download (JSON + CSV) |
| **Objection / 反对** (GDPR Art. 21) [GDPR only] | Object to processing based on legitimate interest, including profiling | Email |
| **Withdraw consent / 撤回同意** (PIPL Art. 15; GDPR Art. 7(3)) | Withdraw any consent-based processing; doesn't affect lawfulness prior to withdrawal | In-app toggle per purpose |
| **Refuse automated decision / 拒绝自动化决策** (PIPL Art. 24; GDPR Art. 22) | Request human review of automated decisions with significant impact | Email |
| **Lodge complaint / 投诉** | With the CAC (China), your EU supervisory authority, or us | See §13 contact |
| **Deceased user's relatives** (PIPL Art. 49) | Close relatives may exercise rights for legitimate purposes unless the deceased opted out before death | Email with proof of relationship |

We may ask you to verify your identity before honoring a request. We may decline manifestly unfounded or excessive requests, stating reasons (GDPR Art. 12(5); PIPL Art. 50).

---

## 9. Algorithmic Decision-Making and Profiling / 自动化决策

- We use rule-based and ML-assisted scoring for **fraud detection** at booking and payment. A block triggered by this system is reviewed by a human within 24 hours upon your request.
- Guide search results are ranked by a combination of relevance, reviews, availability, and pricing. This ranking is not "decision-making" in the PIPL Art. 24 / GDPR Art. 22 sense, but per PIPL Art. 24 para. 2 we offer Tourists a "non-personalized" search option in app settings.
- We do **not** engage in pricing personalization based on User identity ("大数据杀熟" — explicitly prohibited under PIPL Art. 24 para. 2 and 《互联网信息服务算法推荐管理规定》Art. 21).

---

## 10. Cookies, SDKs, and Tracking / Cookie 与 SDK 说明

We use:

| Type | Purpose | Lawful basis | Consent required? |
|---|---|---|---|
| **Strictly necessary** (session, auth, CSRF) | Run the Service | Contract / legitimate interest | No |
| **Functional** (language preference, currency) | Remember choices | Legitimate interest | No (but disclosed) |
| **Analytics** (aggregated usage) | Improve service | Consent | **Yes — opt-in for EEA**; opt-in for non-essential per PIPL practice |
| **Marketing** (push, retargeting) | Marketing | Consent | **Yes — opt-in** |

EEA Tourists see a GDPR/ePrivacy-compliant cookie banner with granular toggles. Non-EEA Users see a PIPL-aligned consent flow. We log and timestamp consent.

Embedded SDKs (Tencent IM SDK, Amap SDK, crash-reporting SDK) are listed with version, purpose, and data accessed at [URL: /sdk-list]. This list is updated within 7 days of any change (per 《App违法违规收集使用个人信息行为认定方法》).

---

## 11. Children and Minors / 未成年人

- **Under 14 — China:** PI of minors under 14 is **sensitive PI** under PIPL Art. 31. We require **guardian consent** before collection. Processing follows 《儿童个人信息网络保护规定》(Children's Online PI Protection Rules).
- **Under 16 — EEA:** GDPR Art. 8 sets the digital consent age at 16 (or as low as 13 under Member State law). We default to 16 for EEA Users; where the Member State sets a lower age, that applies. Guardian consent required below the applicable age.
- **Tourist accounts:** restricted to users **18+**. A minor can be a beneficiary of a booking made by an adult account holder, but the Tourist account itself must be an adult's.
- **Guides must be 18+** (also a 导游证 prerequisite).

If we learn we have inadvertently collected a minor's PI without proper consent, we delete it promptly and notify the guardian where contact is available.

---

## 12. Security and Breach Notification / 安全与泄露通知

### 12.1 Security measures
- Encryption in transit (TLS 1.2+) and at rest (AES-256).
- Role-based access control; least privilege; quarterly access reviews.
- Annual third-party penetration test; continuous vulnerability scanning.
- Employee training; confidentiality and data-handling clauses in all employment / contractor agreements.
- Incident response plan with defined RACI and timelines.

### 12.2 Breach notification commitments
- **PIPL Art. 57:** in the event of a leak, alteration, or loss of PI (or likelihood thereof) we will:
  1. Take immediate remedial action.
  2. Notify the relevant authority (CAC and/or sector regulator) and affected individuals **without undue delay**, **except** where the measures we take can effectively avoid harm — in which case we may not need to notify individuals, subject to the authority's instructions.
- **GDPR Art. 33:** notify the lead supervisory authority within **72 hours** of becoming aware where the breach is likely to result in risk to rights and freedoms.
- **GDPR Art. 34:** notify affected EEA data subjects without undue delay where the breach is likely to result in **high** risk.
- Notification will include: nature of breach, categories and approximate numbers affected, likely consequences, measures taken, and contact for further information.

---

## 13. Contact / 联系方式

### 13.1 Personal Information Protection Responsible Person / 个人信息保护负责人 (PIPL Art. 52)
- Name: [TBD — appoint before launch]
- Email: dpo@ctrip-guides.example
- Postal: [PRC registered office]

### 13.2 GDPR EU Representative (Art. 27) [GDPR only]
- Entity: [TBD — appoint EU-based representative before EEA launch]
- Email: eu-rep@ctrip-guides.example
- Postal: [EU Member State address]

### 13.3 General privacy inquiries
- privacy@ctrip-guides.example
- In-app: Settings → Privacy → Contact DPO

### 13.4 Supervisory authorities
- **China:** Cyberspace Administration of China (CAC, 国家互联网信息办公室); 12377 reporting hotline.
- **EEA:** the supervisory authority of your habitual residence, place of work, or place of the alleged infringement (GDPR Art. 77). A list is maintained by the EDPB.

---

## 14. Changes to This Policy / 政策变更

We will notify Users of material changes via in-app notice and email at least **30 days** before they take effect, except where a shorter period is required by law. Continued use after the effective date constitutes acceptance for non-consent-based processing; **for any new consent-based processing, we will obtain fresh consent — silence is not consent.** (PIPL Art. 14; GDPR Art. 7(2).)

---

## 15. Governing Law and Conflicts / 适用法律

- For Users in mainland China, this Policy is interpreted under PRC law.
- For EEA Tourists, the data-protection provisions are interpreted in accordance with GDPR and applicable Member State law.
- Where PIPL and GDPR conflict, the **stricter standard applies**. Where they are simply different, the regime applicable to the User governs.

---

## ⚠️ Open Items Flagged for Counsel

| # | Item | Why it matters | Suggested action |
|---|---|---|---|
| 1 | Confirm Airwallex is independent controller vs. joint controller | Determines § 5.1 framing, allocation of breach notification | Review Airwallex MSA / DPA |
| 2 | Appoint PIPL 负责人 and GDPR Art. 27 representative | Both required; missing one is a launch blocker | Recruit / contract |
| 3 | CAC Standard Contract filing | Required before any cross-border transfer of PRC-resident PI | File with provincial CAC before launch |
| 4 | Transfer Impact Assessment (TIA) for EEA → China flow | Post-Schrems II requirement | Commission TIA; supplementary measures |
| 5 | Confirm Guide credential retention 5 yrs vs. 2 yrs post-deactivation | Proportionality / minimization | Counsel + product decision |
| 6 | Confirm whether Tourist data is **mirrored** abroad or only accessed on demand | Determines volume calc for PIPL Art. 38 threshold | Architect to confirm |
| 7 | Confirm fraud-detection vendor identity + location | Cross-border + DPA implications | Procurement + Legal |
| 8 | Language-controls clause (this Policy vs. CN translation) | Conflict-of-language risk | Counsel decision |
| 9 | Sensitive PI separate-consent UX flows | Must be granular, not bundled (PIPL Art. 29 strict) | Product + Legal review of UI |
| 10 | Children PI procedures + age-gate UX | Especially for EEA Art. 8 variation | Product + Legal |

---

**END OF DRAFT — REPEAT: NOT FINAL LEGAL ADVICE. ALL PROVISIONS REQUIRE QUALIFIED ATTORNEY REVIEW IN BOTH PRC AND EEA JURISDICTIONS BEFORE PUBLICATION.**