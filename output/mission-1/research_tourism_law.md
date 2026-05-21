# Research Memo — China Tourism Licensing for Guide-Matching Platforms

**To:** Legal, Architect, Orchestrator
**From:** Researcher
**Date:** 2026-05-21
**Re:** Licensing risk for a guide-matching platform under PRC tourism law
**Status:** Draft — **web search returned 0 results this session** (tooling failure, not a finding). All citations below are from my training corpus and must be re-verified by Legal counsel against the live 国家法律法规数据库 (flk.npc.gov.cn) and 文化和旅游部 (MCT) site before any commercial decision is made.

---

## 🚩 Verification Status Legend

- ✅ **VERIFIED** — high-confidence from primary sources (statute text, MCT regulations) reproduced in my training
- 🟡 **INFERRED** — based on cross-reading of statutes and industry practice; needs counsel confirmation
- 🔴 **UNVERIFIED** — could not confirm in this session (e.g., 2024–2026 enforcement actions); flagged for human verification
- ❌ **GAP** — no reliable information; needs primary research

---

## Q1. Tourism Law (旅游法, 2013) — Who Needs a 旅行社业务经营许可证?

### Statutory basis ✅
The **Tourism Law of the People's Republic of China** (中华人民共和国旅游法), adopted by the NPC Standing Committee on **2013-04-25**, effective **2013-10-01**, latest amendments **2016** and **2018** (technical, mainly cross-references). Operative articles:

- **Article 28 (旅游法第二十八条)**: *"设立旅行社，应当具备下列条件……并依法办理工商登记，取得旅行社业务经营许可。"* → Establishing a travel agency requires meeting capital/management conditions **and obtaining a travel-agency business operating permit**. ✅
- **Article 29**: Outbound tour-organizing requires an additional outbound permit. ✅
- **Article 95**: Penalties for operating without a permit (see Q5). ✅

### What counts as "travel agency business"? ✅ / 🟡
The Tourism Law cross-references the **Regulation on Travel Agencies (旅行社条例, State Council Decree No. 550, 2009, amended 2013, 2016, 2020)**.

- **旅行社条例 Article 2** defines 旅行社业务 as: *"招徕、组织、接待旅游者，为其提供相关旅游服务，开展国内旅游业务、入境旅游业务或者出境旅游业务的经营活动。"* → **soliciting, organizing, receiving** tourists and providing related tourism services for **domestic / inbound / outbound** business. ✅
- The three "招徕、组织、接待" verbs are the legal trigger. 🟡 **Industry interpretation** (per MCT enforcement guidance circulars I recall but cannot re-cite in this session): doing **any one** of these for consideration on a routine commercial basis triggers the permit requirement. 🔴 needs Legal to re-verify.

### Activities that clearly trigger the requirement 🟡
1. Selling pre-assembled "tour packages" (跟团游) — clearly in.
2. Selling components bundled into an itinerary (transport + lodging + guide together) — clearly in.
3. **"Soliciting and organizing"** tourists for a fee, even without bundling — 🟡 **likely in** under Article 2's plain language; this is the dangerous middle zone for our platform.
4. Acting as agent (代理) for a licensed travel agency's products — needs **代理业务备案**, not a separate full license. 🟡

---

## Q2. Is a Pure Guide-Matching Platform a "Travel Agency"?

### Short answer
🟡 **High legal risk that yes, it is** — under the plain text of 旅行社条例 Art. 2, "soliciting and organizing tourists … providing related tourism services" arguably covers matching tourists to a guide even with no bundled transport/lodging.

### Reasoning
- The word **"组织" (organize)** is broad. MCT enforcement has historically read it functionally: if the platform is the commercial counterparty the tourist contracts with, the platform is "organizing." 🟡
- **Counter-argument** (information-service framing): if the platform is a **pure marketplace** where (a) the contract of service is **directly between tourist and guide**, (b) the platform never holds itself out as the service provider, (c) the platform charges only an **information/matching fee** (not a tour price), and (d) the platform never markets itinerary content — then it can be argued to be 信息技术服务, analogous to a classifieds board. 🟡
- **Precedent risk**: Several P2P-style tourism startups in 2017–2019 were subject to enforcement under exactly this theory (e.g., the well-known "在路上" / "要出发" -class enforcement debates). 🔴 I cannot re-cite specific case numbers in this session — flag for Legal.

### The 导游 自由执业 (free-practice) pilot — important nuance ✅ / 🟡
- MCT issued **《关于开展导游自由执业试点工作的通知》** in **2016** (pilot launched in **Jiangsu, Zhejiang, Shanghai, Guangdong, Jilin** and expanded). ✅
- Under the pilot, **certified guides may contract directly with tourists** (i.e., outside the traditional rule that guides must be dispatched by a travel agency). ✅
- This pilot is the **single most important regulatory foothold** for a guide-matching platform: in pilot regions the underlying transaction (tourist↔guide) is **lawful without a travel-agency intermediary**, which strengthens the "information service" framing for the platform.
- 🔴 **NEEDS VERIFICATION**: current list of pilot cities/provinces in 2025–2026 and whether the pilot has been made permanent or rolled back. I recall expansion announcements but cannot confirm post-2023 status.

### Architect note
This directly maps to the **Path B + C hybrid** in PRD v1.2 §0: in pilot cities, use the "self-practice" partner row; in non-pilot cities, route bookings through a licensed travel-agency partner. The legal logic above is what makes that split defensible.

---

## Q3. Three License Concepts — Compared

| Aspect | 旅行社业务经营许可证 | 在线旅游经营服务 (2020 OTA regs) | 信息技术服务 (pure platform) |
|---|---|---|---|
| **Authority** | 文化和旅游部 / provincial 文旅厅 | 文化和旅游部 (regulation only, not a separate permit) | 工信部 ICP + market supervision; no tourism-specific permit |
| **Primary source** ✅ | 旅游法 art. 28; 旅行社条例 art. 2, 6–8 | 《在线旅游经营服务管理暂行规定》, MCT Order No. 4, **effective 2020-10-01** | Telecoms regs; 电子商务法 (2019) |
| **What it authorizes** | Conducting 旅行社业务 (soliciting/organizing/receiving tourists) | **Not a separate license** — it's the **conduct rules** for online platforms that engage in tourism operations | Operating an information/matching technology service |
| **Capital / staff requirements** | RMB 300,000 (domestic+inbound) / RMB 1,500,000 (outbound) registered capital + qualified staff (旅行社条例 art. 6) ✅ | None additional — but **if you do tourism operations online, you must ALSO hold the underlying tourism license** (see 暂行规定 art. 7) ✅ | None tourism-specific; ICP filing/license per ordinary internet-business rules |
| **Quality deposit (质量保证金)** | Yes — 旅行社条例 art. 15: RMB 200K / 1.4M depending on scope ✅ | N/A (deposit attaches to the underlying agency) | N/A |
| **Key obligations** | Contract templates, mandatory insurance (责任险), guide dispatch rules | Real-name verification, info disclosure, algorithmic ranking transparency, complaint handling within 5 business days, cooperate with regulator data calls | Standard e-commerce platform duties under 电子商务法 arts. 27, 38 |
| **Can a pure marketplace claim this?** | — | — | 🟡 **Only if it does not engage in 旅行社业务 as defined in art. 2** |

### Critical clarification ✅
**在线旅游经营服务管理暂行规定 (2020) Article 7** explicitly says: *"在线旅游经营者应当依法取得相应的经营许可或者办理工商登记"* → online tourism operators must obtain the **corresponding** business permit (i.e., the underlying 旅行社 permit if doing travel-agency business). The 2020 reg is **layered on top of**, not a substitute for, the 旅行社 permit.

🔴 **NEEDS VERIFICATION**: whether the 2020 暂行规定 has been replaced or amended by a formal 规定 (non-interim) in 2024–2026. I have no confirmed update post-2023.

---

## Q4. How Existing Platforms Handle It

### Trip.com / Ctrip (携程) ✅
- Operating entity in PRC: **上海携程国际旅行社有限公司** and various provincial subsidiaries — i.e., they hold **full 旅行社业务经营许可证** (domestic, inbound, **and** outbound — outbound permit is the hardest tier). ✅
- They classify themselves as a **travel agency that also operates an OTA platform** — not as a pure information service. This is the conservative, safe model.
- Trip.com Group is listed on NASDAQ; their 20-F filings disclose the travel-agency license dependency as a material risk factor. 🟡

### Klook 🟡 / 🔴
- HK-headquartered. Their PRC operating entity (per my recollection) is **客路（上海）国际旅行社有限公司** or similar — they hold a **PRC travel-agency license** to legally sell experience products to PRC outbound and inbound tourists. 🟡 needs corporate-records re-pull from 国家企业信用信息公示系统.
- For inbound tourists (foreigners coming to China), the bookings flow on the Hong Kong / SG entity; PRC delivery is sub-contracted to licensed local operators. 🟡

### GetYourGuide 🟡 / 🔴
- Berlin-HQ. **Limited mainland China retail presence** historically. They list China experiences but the contracting entity has typically been EU-based with local supplier sub-contracts. 🟡 no public confirmation of a PRC travel-agency license — needs Legal to check 公示系统.

### Smaller PRC guide-booking platforms 🔴
- 8只小猪 (8xiaozhu), 妙游 (Miaoyou), 海玩 etc. — most either (a) obtained a 旅行社 license themselves, or (b) partnered with one. 🔴 specific corporate structures not re-verified this session.
- ❌ **GAP**: I cannot confirm in this session whether any pure-information-service guide platform has operated long-term in PRC without a travel-agency license or partner. The empirical answer matters a lot for risk-pricing.

---

## Q5. Penalties for Operating Without the License ✅

Primary basis — **旅游法 Article 95** and **旅行社条例 Article 47**:

- **未经许可经营旅行社业务** (operating travel-agency business without a permit):
  - Order to cease operations
  - **Confiscation of illegal gains**
  - Fine of **RMB 100,000 – 500,000**
  - If illegal gains exceed RMB 100,000: fine of **2× to 5× illegal gains**
  - Severe cases: order business closure / revocation of business registration
- Personal liability: legal representative and directly responsible managers may be **personally fined RMB 20,000 – 50,000**. ✅ (旅行社条例 art. 47)
- 🟡 In practice, regional 文旅 enforcement has also frozen platform domains and required ICP filings to be withdrawn.

**Criminal exposure** 🟡:
- If conduct constitutes **非法经营罪 (illegal business operations, 刑法 art. 225)** — possible 5+ years imprisonment plus fine. This requires "serious circumstances" and is not the default for licensing violations, but has been used in egregious cases. 🔴 case law in tourism specifically needs separate research.

---

## Q6. 2024–2026 Regulatory Changes / Enforcement Actions

🔴 **LOW CONFIDENCE — web search returned no results this session.** I can offer the following based on training cutoff:

- 🟡 The **导游自由执业试点** has reportedly continued and possibly been extended to additional provinces; I cannot confirm post-2023 status.
- 🟡 **文化和旅游部 "黑名单" (blacklist) of unlicensed online tourism operators** — periodic releases since 2021. Platforms named have included unlicensed WeChat-mini-program operators. Status of 2024–2026 releases unverified.
- 🔴 Whether **在线旅游经营服务管理暂行规定 (2020)** has been replaced by a permanent regulation — unverified.
- 🔴 Any 2024–2026 enforcement targeting **foreign-tourist-facing inbound platforms** (which is our market) — unverified. The 2024 visa-free expansion for many Western/ASEAN nationals likely increased regulator attention on inbound tourism quality; specific enforcement trends need a fresh sweep of MCT news.

**Recommended next-step research (assign back to Researcher with working web search):**
1. Pull latest 文旅部 公告 / 通报 list for 2024–2026 on online tourism enforcement.
2. Confirm current list of 自由执业 pilot regions.
3. Pull corporate-records (国家企业信用信息公示系统) for Klook and GetYourGuide PRC entities, if any.
4. Search for case law / administrative penalty decisions (中国裁判文书网 + 信用中国) using 关键词 "未经许可经营旅行社业务" 2024–2026.

---

## 🎯 Bottom Line for the PRD

1. **A pure-platform / 信息技术服务 framing is *defensible but not safe*** on its own. The plain text of 旅行社条例 art. 2 is broad, and the 2020 OTA regulation (art. 7) explicitly requires the underlying permit.
2. **The PRD v1.2 Path B + C hybrid is the right shape**:
   - In **导游自由执业** pilot cities → "self-practice partner" row is lawful, platform acts as information service. **This is the cleanest legal posture.**
   - Outside pilot cities → bookings must route through a **licensed 旅行社 partner** with valid 旅行社业务经营许可证. The partner is the legal counterparty for "organizing" the tourist.
3. **Hard requirement**: before MVP, Legal must obtain (a) confirmed current pilot-city list, (b) at least one signed travel-agency partner agreement per non-pilot MVP city, (c) verification that platform-side marketing copy does not hold the platform out as the tour organizer (linter from PRD §6 enforces this).
4. **Penalty exposure if we get it wrong**: RMB 100K–500K + 2–5× illegal gains + personal liability for officers. **Material — do not launch without Legal sign-off on C-01.**

---

## ⚠️ Tooling Note for Orchestrator

The web search tool returned **"No results found"** for `China tour guide license 导游证 requirements 2025`. I proceeded on training-corpus knowledge for this memo because the question is time-critical, but **every 🔴 flag above is a known gap that requires a working search** before this memo can be relied upon for a launch decision. Please re-queue Q6 once search is restored.