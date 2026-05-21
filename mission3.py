"""
Mission 3: Generate All Legal Documents (Path B)

FLOW: Legal (draft all docs) → Researcher (verify completeness) → Legal (finalize)
DELIVERABLE: ToS, Privacy Policy, Guide Agreement — all Path B compliant
"""
import sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.message_bus import MessageBus, Message, MessageType
from src.agents.legal import LegalAgent
from src.agents.researcher import ResearcherAgent


def main():
    print("=" * 70)
    print("🎯 MISSION 3: GENERATE LEGAL DOCUMENTS (Path B)")
    print("=" * 70)
    print()
    print("Deliverables: ToS, Privacy Policy, Guide Service Agreement")
    print("Flow: Legal → Researcher (verify) → Legal (finalize)")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    start = time.time()
    bus = MessageBus()
    legal = LegalAgent(bus)
    researcher = ResearcherAgent(bus)
    results = {}

    # Load Mission 1+2 context
    m2_legal = ""
    if os.path.exists("output/mission-2/legal_constraints.md"):
        with open("output/mission-2/legal_constraints.md") as f:
            m2_legal = f.read()[:3000]

    log = lambda step, detail="": print(f"\n{'='*70}\n[{time.strftime('%H:%M:%S')}] MISSION 3 — {step}\n  {detail}\n{'='*70}")

    # ================================================================
    # STEP 1: Legal — Draft Terms of Service
    # ================================================================
    log("STEP 1/5", "Legal: Draft Terms of Service")

    bus.post(Message(
        sender="mission",
        recipient="legal",
        msg_type=MessageType.REQUEST,
        subject="Draft Terms of Service — Path B pure platform",
        payload=f"""Draft the Terms of Service for Ctrip-Guides platform.

PLATFORM FACTS:
- Name: Ctrip-Guides (working name)
- Model: Information service platform connecting tourists with independent licensed guides
- Path B: We are NOT a travel agency. We facilitate connections only.
- Revenue: 12% information service fee (信息服务费) on each completed connection
- Payment: Tourist pays via Airwallex (licensed PSP holds funds) → guide receives CNY payout
- Guides: Independent contractors with valid 导游证, set own prices, accept/decline freely
- Markets: Beijing, Shanghai, Xi'an, Chengdu
- Users: Foreign tourists (primarily US, UK, EU, Australia) + Chinese guides

PATH B LEGAL CONSTRAINTS (from Mission 2):
{m2_legal[:2000]}

REQUIREMENTS FOR THE ToS:
1. Written in English (primary) — note that Chinese translation will be provided separately
2. Must clearly establish platform as information intermediary, NOT tour operator
3. Must define the three-party relationship: platform ↔ tourist ↔ guide
4. Must specify that guide services are provided by independent guides, not by us
5. Must include: dispute resolution, liability limitations, cancellation policy framework
   (but cancellation terms are set by each guide, not by platform)
6. Must include governing law clause (consider: PRC law for CN operations, 
   with arbitration in HK for international disputes)
7. Must address: account terms, prohibited conduct, IP rights, 
   user-generated content (reviews), data handling reference (point to Privacy Policy)
8. Must include PIPL + GDPR compliant data handling section (or cross-reference)
9. Must include MCT Order No. 4 required disclosures
10. Must include the defensive platform-role disclaimer from Mission 2 Legal review

Output the FULL ToS text, ready for attorney review. Mark sections needing 
jurisdiction-specific counsel input with [COUNSEL REVIEW]."""
    ))

    responses = legal.receive_and_process()
    tos = responses[0].payload if responses else "FAILED"
    results["tos"] = tos
    print(f"\n📜 Legal produced Terms of Service ({len(tos):,} chars)")

    # ================================================================
    # STEP 2: Legal — Draft Privacy Policy
    # ================================================================
    log("STEP 2/5", "Legal: Draft Privacy Policy (PIPL + GDPR)")

    bus.post(Message(
        sender="mission",
        recipient="legal",
        msg_type=MessageType.REQUEST,
        subject="Draft Privacy Policy — PIPL + GDPR dual compliance",
        payload="""Draft the Privacy Policy for Ctrip-Guides platform.

DUAL COMPLIANCE: Must satisfy BOTH:
- China PIPL (个人信息保护法) — for all users, data processed in China
- EU GDPR — for EU tourist users

DATA WE COLLECT AND PROCESS:
Tourists:
- Account: name, email, phone, country, preferred language/currency
- Booking: guide selected, dates, service type, payment amount
- Payment: card details (held by Airwallex, NOT by us), transaction records
- Communication: chat messages (auto-translated), support tickets
- Location: city-level only (no GPS tracking), unless tourist opts into meeting-point sharing
- Reviews: star rating, text content
- Device: IP address, browser/device type, language settings

Guides:
- Account: name, email, phone, city, languages spoken, specialties
- Credential: 导游证 number, issuing authority, photo of license (for verification)
- Availability: calendar data, pricing
- Payment: bank account / Alipay / WeChat Pay ID for payout
- Reviews: star rating, text content
- Earnings: transaction history, payout records

REQUIREMENTS:
1. Separate sections for PIPL and GDPR obligations
2. Explicit lawful basis per processing purpose (PIPL Art. 13; GDPR Art. 6)
3. Cross-border data transfer disclosure (PIPL Art. 38-39; GDPR Ch. V)
4. Data subject rights (access, correction, deletion, portability)
5. Data retention periods per category
6. Third-party data sharing disclosure (Airwallex, Tencent IM, Tencent MT, Amap)
7. Cookie/tracking disclosure
8. Children/minors policy (PIPL Art. 31; GDPR special provisions)
9. Breach notification commitment
10. Contact info for data protection inquiries + PIPL responsible person

Output the FULL Privacy Policy text. Mark [COUNSEL REVIEW] where needed."""
    ))

    responses = legal.receive_and_process()
    privacy = responses[0].payload if responses else "FAILED"
    results["privacy_policy"] = privacy
    print(f"\n🔒 Legal produced Privacy Policy ({len(privacy):,} chars)")

    # ================================================================
    # STEP 3: Legal — Draft Guide Service Agreement
    # ================================================================
    log("STEP 3/5", "Legal: Draft Guide Service Agreement")

    bus.post(Message(
        sender="mission",
        recipient="legal",
        msg_type=MessageType.REQUEST,
        subject="Draft Guide Service Agreement — independent contractor",
        payload="""Draft the Guide Service Agreement for Ctrip-Guides platform.
This is the contract between the platform and each guide.

CRITICAL: Must establish INDEPENDENT CONTRACTOR relationship, NOT employment.

KEY TERMS:
- Guide is an independent service provider with valid 导游证
- Guide sets own prices, availability, and service terms
- Guide accepts/declines service requests freely
- No exclusivity — guide can list on competing platforms
- Platform takes 12% information service fee (信息服务费) from each completed service
- Platform verifies 导游证 but does not issue, supervise, or manage guide work
- Guide is responsible for: their own taxes (劳务报酬所得), insurance, compliance
- Platform provides: matching technology, payment processing, translation tools
- Either party can terminate with 30 days notice

MUST INCLUDE:
1. Parties and recitals (platform = information service provider)
2. Scope of relationship (information service, NOT employment/agency)
3. Guide obligations (valid license, professional conduct, own insurance)
4. Platform obligations (tech platform, payment facilitation, credential display)
5. Fee structure and payment terms (12% info service fee, T+3 settlement)
6. IP rights (guide owns their content; platform has display license)
7. Cancellation and no-show terms (guide-set, platform facilitates)
8. Liability and indemnification
9. Data handling (cross-reference Privacy Policy)
10. Termination (mutual 30-day notice; immediate for license revocation)
11. Dispute resolution (same as ToS)
12. Governing law
13. Independent contractor classification safeguards per Mission 2 Legal R4

BILINGUAL: Produce in English. Note that Chinese version needed for PRC guides.
Mark [COUNSEL REVIEW] where needed."""
    ))

    responses = legal.receive_and_process()
    guide_agreement = responses[0].payload if responses else "FAILED"
    results["guide_agreement"] = guide_agreement
    print(f"\n🤝 Legal produced Guide Agreement ({len(guide_agreement):,} chars)")

    # ================================================================
    # STEP 4: Researcher — Verify completeness against competitors
    # ================================================================
    log("STEP 4/5", "Researcher: Verify legal docs against competitor standards")

    legal.handoff_to(
        "researcher",
        "Verify legal documents completeness",
        f"""Legal produced 3 documents. Verify they are complete by researching:

1. What do Klook, GetYourGuide, and Viator's ToS include that ours might be missing?
2. What do similar platform Privacy Policies include for PIPL compliance?
3. Are there any standard clauses in guide/contractor agreements for tourism platforms 
   that we're missing?
4. Any recent (2024-2026) enforcement actions against platforms for deficient ToS or 
   Privacy Policies in China?

Also check:
- Does our ToS properly handle tourist safety/emergency situations?
- Does our Privacy Policy cover all third-party services mentioned in the tech spec?
  (Airwallex, Tencent IM, Tencent MT, Amap, Aliyun)
- Does the Guide Agreement have adequate IP protection for both parties?

ToS summary: {tos[:1500]}
Privacy Policy summary: {privacy[:1500]}
Guide Agreement summary: {guide_agreement[:1500]}

Return: GAPS FOUND (what's missing) and CONFIRMED (what's solid)."""
    )

    responses = researcher.receive_and_process()
    verification = responses[0].payload if responses else "FAILED"
    results["verification"] = verification
    print(f"\n🔍 Researcher produced verification ({len(verification):,} chars)")

    # ================================================================
    # STEP 5: Legal — Issue final sign-off with amendments
    # ================================================================
    log("STEP 5/5", "Legal: Final review and amendments based on verification")

    researcher.handoff_to(
        "legal",
        "Final amendments to legal documents",
        f"""Researcher found gaps in the legal documents. Produce:

1. A list of AMENDMENTS to each document (ToS, Privacy Policy, Guide Agreement)
2. The exact text to add/change for each amendment
3. A final SIGN-OFF CHECKLIST: every requirement from Mission 2 Legal constraints 
   mapped to a specific section in one of the three documents

RESEARCHER GAPS:
{verification[:3000]}

Format as:
## Amendments to ToS
[numbered list of changes with exact text]

## Amendments to Privacy Policy
[numbered list of changes with exact text]

## Amendments to Guide Agreement
[numbered list of changes with exact text]

## Sign-Off Checklist
[table: Requirement | Document | Section | Status]"""
    )

    responses = legal.receive_and_process()
    amendments = responses[0].payload if responses else "FAILED"
    results["amendments"] = amendments
    print(f"\n✅ Legal produced amendments + sign-off ({len(amendments):,} chars)")

    elapsed = time.time() - start

    # Save deliverables
    os.makedirs("output/mission-3", exist_ok=True)

    file_map = {
        "tos": "01_terms_of_service.md",
        "privacy_policy": "02_privacy_policy.md",
        "guide_agreement": "03_guide_service_agreement.md",
        "verification": "04_verification_report.md",
        "amendments": "05_amendments_signoff.md",
    }
    for key, filename in file_map.items():
        with open(f"output/mission-3/{filename}", "w") as f:
            f.write(results.get(key, "FAILED"))

    with open("output/mission-3/DELIVERABLE.md", "w") as f:
        f.write(f"<!-- Mission 3 | {time.strftime('%Y-%m-%d %H:%M:%S')} | {elapsed:.0f}s | Path B -->\n\n")
        f.write("# Ctrip-Guides Legal Document Package\n\n")
        f.write("## Documents Produced\n\n")
        for key, filename in file_map.items():
            size = len(results.get(key, ""))
            f.write(f"- [{filename}](./{filename}) ({size:,} chars)\n")
        f.write(f"\n## Amendments\n\n")
        f.write(results.get("amendments", "NONE"))

    with open("output/mission-3/mission_data.json", "w") as f:
        json.dump({
            "mission": "Legal Document Generation (Path B)",
            "results": results,
            "messages": [m.to_dict() for m in bus.messages],
            "elapsed_seconds": elapsed,
        }, f, indent=2, default=str)

    # Report
    print(f"\n{'='*70}")
    print(f"📊 MISSION 3 COMPLETE")
    print(f"{'='*70}")
    print(f"  Messages: {len(bus.messages)} | Runtime: {elapsed:.0f}s ({elapsed/60:.1f} min)")
    print()
    print("Message flow:")
    for msg in bus.messages:
        icons = {"request": "📨", "response": "📬", "handoff": "🔀"}
        icon = icons.get(msg.msg_type.value, "💬")
        print(f"  {icon} {msg.sender:>12} → {msg.recipient:<12} [{msg.msg_type.value:8}] {msg.subject[:55]}")
    print()
    print("Deliverables:")
    for fn in sorted(os.listdir("output/mission-3")):
        size = os.path.getsize(f"output/mission-3/{fn}")
        print(f"  📄 output/mission-3/{fn} ({size:,} bytes)")
    print(f"\n🏁 Done. Deliverables in output/mission-3/")


if __name__ == "__main__":
    main()
