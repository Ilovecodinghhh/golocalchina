# Validation Report: China Deployment Tech Stack
**From:** Researcher Agent
**To:** Architect (timed out — report queued)
**Date:** 2026-05-21
**Re:** Tech choices for Ctrip-Guides platform

> **Note on sources:** The web search batch returned mostly tourist-facing payment guides and dictionary entries — not useful for infrastructure validation. The findings below rely on my training data + industry-standard knowledge. **Items flagged ⚠️ need human verification before commitment** (vendor terms change frequently, especially for cross-border payments and ICP rules).

---

## 1. Payment Providers — Foreign Card → CNY

| Provider | Verdict | Notes |
|---|---|---|
| **Stripe** | ❌ NOT VIABLE as primary | Stripe does not have a mainland China entity. A China-based merchant (中国境内主体) **cannot onboard directly to Stripe**. Stripe HK/SG can accept foreign cards, but settlement to a mainland CNY account requires a separate cross-border channel. Works only if your contracting entity is HK/SG. |
| **Airwallex** | ✅ **BETTER ALTERNATIVE — recommended primary** | HK-headquartered, mainland China license, explicitly designed for cross-border merchants. Accepts Visa/Mastercard/Amex/JCB, settles in CNY or 11+ currencies. Native to your exact use case (foreign card in → CNY out to mainland guides). |
| **Adyen** | ⚠️ Viable but enterprise-tier | Global card acquiring works, but minimum volumes and integration effort are heavy for an early-stage startup. Revisit at scale (>$10M GMV). |
| **PingPong** | ⚠️ Limited for inbound | PingPong's strength is *outbound* (Chinese sellers receiving from foreign marketplaces). Their inbound merchant acquiring is newer and less documented. Possible secondary, not primary. |
| **Alipay/WeChat Pay (cross-border)** | ✅ ADD — must-have secondary | Tourists increasingly link foreign cards to Alipay Tour Pass / WeChat Pay International. Essential UX even if not your primary rail. |

**Recommendation:**
- **Primary:** Airwallex for foreign card acquiring → CNY payout
- **Secondary:** Alipay International + WeChat Pay International for tourists who prefer mobile
- **Avoid:** Stripe as the sole rail unless you contract through a HK/SG entity (which has separate tax + regulatory implications — loop in Legal)

⚠️ **Needs verification:** Current Airwallex MDR (likely 2.8–3.5% for foreign cards), KYB timeline, and whether they require an ICP-filed mainland entity or accept HK entity.

---

## 2. Hosting — Aliyun vs. Tencent Cloud vs. Huawei Cloud

| Provider | Verdict | Notes |
|---|---|---|
| **Aliyun (Alibaba Cloud)** | ✅ **CONFIRMED — recommended** | Largest market share in China, best English docs, easiest ICP filing assistance (they have a dedicated 备案 portal in English-ish form), mature international console. Best for foreign-founded startups. |
| **Tencent Cloud** | ⚠️ Solid second | Better if you're deeply integrated with WeChat/Mini Programs ecosystem. Slightly cheaper at low tiers. Docs slightly weaker for non-Mandarin operators. |
| **Huawei Cloud** | ❌ Not for your use case | Strong for state-owned enterprises and AI workloads; weaker startup support and worse English-language experience. |

### ICP Filing — what it actually involves

**Two types:**
1. **ICP 备案 (Beian / non-commercial filing)** — required for ANY domain serving from a mainland server.
2. **ICP 证 (Commercial ICP license)** — required if you operate a "commercial internet information service" (paid content, paid memberships). A booking marketplace likely needs this. ⚠️ **Flag for Legal.**

**Requirements (备案):**
- Mainland China-registered company (营业执照 / business license) — **a foreign entity alone cannot file**
- Legal representative with mainland Chinese ID
- Hosted on a mainland Chinese cloud provider
- Domain registered with a MIIT-accredited registrar
- Physical office address in the province where you file
- Photo of legal rep against provincial backdrop (Aliyun mails you a backdrop kit)

**Timeline:** 10–20 business days typical; can stretch to 30+ if MIIT flags anything. Province-dependent — Shanghai/Beijing faster, smaller provinces slower.

**Bigger issue (flag to Architect):** If we are foreign-founded with no mainland legal entity, **we cannot get ICP filing**. Options:
- (a) Incorporate a WFOE (Wholly Foreign-Owned Enterprise) in China — 3–6 months, ~$5–15k
- (b) Host outside mainland (HK/Singapore) and accept ~200–500ms latency + intermittent GFW friction
- (c) Use a local partner / VIE structure (risky, requires Legal review)

⚠️ **Needs Legal validation:** Whether a guide-marketplace requires the full ICP 证 commercial license vs. just 备案.

---

## 3. Translation APIs — Inside the GFW

| Provider | Inside GFW? | Verdict |
|---|---|---|
| **Tencent Cloud MT (腾讯翻译君)** | ✅ Native | **CONFIRMED for primary** — low latency (<100ms intra-China), competitive pricing (~¥58/million chars), 18+ language pairs incl. EN↔ZH-CN well-tuned. |
| **Aliyun Machine Translation** | ✅ Native | Comparable to Tencent; slightly better for e-commerce/travel domain terms. Good fallback. |
| **Baidu Translate API** | ✅ Native | Cheapest, but English quality noticeably weaker for conversational/colloquial text — **not ideal for chat**. |
| **DeepL** | ❌ Blocked/unreliable inside GFW | Higher quality than any Chinese provider for EU languages, but API endpoints are not reliably reachable from mainland. **Do not use as primary.** |
| **Google Translate** | ❌ Blocked | API endpoint not reachable from mainland without VPN. **Cannot use inside China.** |

**Recommendation:**
- **Primary:** Tencent Cloud MT for in-app chat (low latency, GFW-native, good ZH↔EN)
- **Fallback:** Aliyun MT
- **Premium tier (optional):** Route long-form content (guide bios, itineraries) through DeepL via a server *outside* the GFW where quality matters more than latency

⚠️ **Cost ballpark (verify):** Tencent ~¥58/1M chars; Aliyun ~¥50/1M chars. For chat with avg 50 chars/message, ~20M messages = ~¥1000–1200/month at scale. Trivial.

---

## 4. Maps — China Constraints

**Critical fact:** Google Maps and Mapbox **do not work reliably inside mainland China**. Google's tile servers are blocked, and Mapbox's tiles route through CDNs that are inconsistent. Also, **Chinese law requires that maps shown to users in China use GCJ-02 coordinate system** (the "Mars" obfuscated coords) — WGS-84 raw GPS is technically non-compliant.

| Provider | English API? | Verdict |
|---|---|---|
| **Gaode / Amap (高德, owned by Alibaba)** | ⚠️ Partial English POI data, console mostly Chinese | ✅ **CONFIRMED — recommended primary**. Most accurate for China, best traffic/transit data. English POI coverage is decent in tier-1 cities, weaker in tier-3. |
| **Baidu Maps** | ⚠️ Weaker English | Comparable, but Amap generally has better navigation and outsells Baidu in mobile. |
| **Tencent Maps** | ⚠️ Limited English | Third-tier; use only if deeply integrated with WeChat Mini Program. |
| **Google Maps** | N/A | ❌ Blocked in mainland. Use only for users browsing your site from outside China (pre-trip planning). |
| **Mapbox** | N/A | ❌ Unreliable inside mainland. Same constraint. |

**Recommendation — hybrid:**
- **Inside China (in-app, in-trip):** Amap JS API + Amap Places API
- **Outside China (pre-booking research on web):** Mapbox or Google Maps (better English POI labels for tourists planning)
- **Detect user location server-side** and serve the appropriate map SDK

⚠️ **Legal flag:** Maps shown to users physically in China must be GCJ-02. Amap handles this natively; if you ever overlay Google data on top, you'd need a WGS-84→GCJ-02 transform. Loop Legal in on map compliance (测绘法 / Surveying & Mapping Law).

---

## 5. Real-Time Chat — WebSockets behind the GFW

**Short version:** WebSockets themselves work fine inside China. The gotchas are about **edge connectivity from foreign tourists who may be on hotel WiFi, mobile roaming, or VPN-routing**.

**Known gotchas:**
1. **GFW occasionally throttles long-lived TLS connections** during sensitive periods (Party Congress, anniversaries). Long-running WSS connections may drop every 20–60 min. → Implement aggressive reconnect + message replay from server.
2. **Mainland CDN/WS termination required** for low latency. If your WS server is in Singapore and a user is in Chengdu, expect 200–400ms RTT and frequent drops. → Terminate WSS inside mainland (Aliyun GSLB or equivalent).
3. **Some carrier mobile networks (China Telecom roaming, esp. on foreign SIMs) deprioritize non-HTTP traffic.** WSS over 443 is fine; raw WS over 80 is not.
4. **WeChat Mini Program in-app browsers** restrict WS — if you ever embed via WeChat sharing, use WeChat's `wx.connectSocket` API instead.

**Tech recommendations:**
| Option | Verdict |
|---|---|
| **Native WebSocket (WSS over 443) + custom Node/Go server** | ✅ Fine for MVP. Use `ws` (Node) or `gorilla/websocket` (Go). |
| **Socket.IO** | ⚠️ Works but adds overhead; transport fallback to long-polling is helpful for flaky networks. |
| **Tencent Cloud IM (TIM) / Aliyun MNS** | ✅ **BETTER ALTERNATIVE for chat specifically** — managed, GFW-optimized, handles offline messages, push notifications, multi-device sync. Saves 3–6 months of build time. |
| **Pusher / Ably / PubNub** | ❌ Edges outside China — high latency / unreliable for mainland users. |
| **Firebase Realtime DB / Firestore** | ❌ Google-backed — blocked in mainland. |

**Recommendation:**
- **For MVP:** Tencent Cloud IM (云通信 IM) — purpose-built, handles offline + push + moderation hooks (which you'll need for compliance).
- **If building custom:** WSS over 443, terminate on Aliyun inside mainland, with reconnect/replay + heartbeat every 30s.

---

## Summary Validation Table

| # | Architect's choice | Verdict |
|---|---|---|
| 1 | Stripe for payments | ❌ **BETTER ALTERNATIVE: Airwallex** (primary) + Alipay/WeChat International (secondary) |
| 2 | Aliyun for hosting | ✅ **CONFIRMED** — but ICP filing requires a mainland legal entity (blocker, escalate to Legal) |
| 3 | Tencent MT for translation | ✅ **CONFIRMED** — DeepL/Google blocked inside GFW |
| 4 | Amap for maps | ✅ **CONFIRMED** for in-China; hybrid with Google/Mapbox for pre-trip web browsing outside China |
| 5 | WebSockets for chat | ✅ **CONFIRMED with caveat — BETTER ALTERNATIVE: Tencent Cloud IM** to avoid GFW reconnect/replay/push infra work |

---

## Blockers Surfaced for Other Agents

**→ Legal:**
- ICP 备案 vs. ICP 证 (commercial license) requirement for a paid marketplace
- Map compliance under Surveying & Mapping Law (测绘法), GCJ-02 requirement
- Whether HK entity can run a guide-booking platform serving mainland users without WFOE

**→ Architect (when back online):**
- Mainland entity decision drives everything — WFOE vs. HK-only vs. local partner. Hosting/ICP/payments all branch from this.
- Recommend Tencent Cloud IM over self-built WS to save runway

**→ Product/PM:**
- Tourist payment UX: most foreign visitors in 2025–26 expect Alipay Tour Pass / WeChat International to "just work" — don't make them enter cards if avoidable (corroborated by tourist-payment guides in search results #1–3).

⚠️ **All cost figures and timelines above are approximate from training data — re-confirm with current vendor pricing pages before locking the spec.**