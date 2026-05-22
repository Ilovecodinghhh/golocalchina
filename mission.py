"""
Mission Runner — Executes scoped missions through the agent pipeline.
"""
import sys
import os
import time
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.message_bus import MessageBus, Message, MessageType


def create_agents(bus):
    from src.agents.researcher import ResearcherAgent
    from src.agents.legal import LegalAgent
    from src.agents.architect import ArchitectAgent
    from src.agents.builder import BuilderAgent
    return {
        "researcher": ResearcherAgent(bus),
        "legal": LegalAgent(bus),
        "architect": ArchitectAgent(bus),
        "builder": BuilderAgent(bus),
    }


def mission_1(bus, agents):
    """
    MISSION 1: Validate the business model is legal in China.
    
    QUESTION: Does a tourist-guide matching platform require a 
    旅行社业务经营许可证 (travel agency business license)? If so, 
    what are the alternatives to operate legally?
    
    FLOW: Researcher → Legal → Researcher (verify) → Legal (final memo)
    DELIVERABLE: GO/NO-GO memo with license requirements + alternatives
    """

    log = lambda step, detail="": print(f"\n{'='*70}\n[{time.strftime('%H:%M:%S')}] MISSION 1 — {step}\n  {detail}\n{'='*70}")
    results = {}

    # ================================================================
    # STEP 1: Researcher — gather facts on China tourism licensing
    # ================================================================
    log("STEP 1/4", "Researcher: Gather facts on China tourism law and licensing")

    bus.post(Message(
        sender="mission",
        recipient="researcher",
        msg_type=MessageType.REQUEST,
        subject="Research China tourism licensing for guide-matching platforms",
        payload="""Research the following specific questions about operating a tourist-guide 
matching platform in China. This is critical — the business may be illegal without the right license.

QUESTIONS:
1. What does China's Tourism Law (旅游法, 2013) say about who needs a 旅行社业务经营许可证 
   (travel agency business license)? What activities trigger the requirement?
   
2. Is a platform that ONLY matches tourists with independent guides (no tour packages, 
   no transport, no accommodation bundling) considered a "travel agency" under the law?
   
3. What is the difference between:
   - 旅行社业务经营许可证 (travel agency license)
   - 在线旅游经营服务 (online tourism business service) under the 2020 regulations
   - 信息技术服务 (information technology service / pure platform model)
   
4. How do existing platforms handle this? Specifically:
   - How does Trip.com/Ctrip classify itself?
   - How do smaller guide-booking platforms (if any) in China operate?
   - What about Klook, GetYourGuide — do they have China entities with tourism licenses?
   
5. What are the penalties for operating without the correct license?

6. Are there any recent (2024-2026) regulatory changes or enforcement actions 
   related to online tourism platforms?

Be specific. Cite article numbers. Flag what you could NOT verify."""
    ))

    responses = agents["researcher"].receive_and_process()
    research_1 = responses[0].payload if responses else "NO RESEARCH"
    results["research_tourism_law"] = research_1
    print(f"\n🔍 Researcher produced tourism law findings ({len(research_1):,} chars)")

    # ================================================================
    # STEP 2: Legal — analyze the research and produce initial opinion
    # ================================================================
    log("STEP 2/4", "Legal: Analyze research findings and classify our business model")

    agents["researcher"].handoff_to(
        "legal",
        "Legal analysis: Does our platform need a 旅行社业务经营许可证?",
        f"""Based on the Researcher's findings below, produce a legal analysis memo.

OUR BUSINESS MODEL:
- Two-sided platform connecting foreign tourists with locally certified guides (持证导游)
- Guides are independent contractors, set their own rates and availability
- Platform takes a commission (15%) on each booking
- Platform handles payment processing (foreign card → CNY payout)
- Platform does NOT bundle transport, accommodation, or tour packages
- Platform verifies guide credentials (导游证) but does not employ guides
- MVP cities: Beijing, Shanghai, Xi'an, Chengdu

ANALYZE:
1. Under 旅游法 and relevant regulations, does this model require a 旅行社业务经营许可证?
   - If YES: what specific activities trigger it? Can we restructure to avoid it?
   - If NO: what license DO we need? What's the legal basis for exemption?

2. What about the "Online Tourism Business" (在线旅游经营服务) category under the 
   2020 文旅部 regulations? Does that apply to us?

3. Produce a decision tree:
   IF we need a travel agency license → what does it take to get one?
   IF we can operate as a pure tech platform → what constraints apply?
   IF there's a middle path → what is it?

4. What are 3 alternative business structures that could work legally?
   (e.g., partner with a licensed agency, operate as information service only, etc.)

5. Rate each path: GREEN (safe), YELLOW (gray area), RED (likely illegal)

RESEARCHER FINDINGS:
{research_1[:6000]}

IMPORTANT: This is a GO/NO-GO decision for the entire business. Be thorough. 
Cite specific articles. Flag assumptions. Mark this as DRAFT FOR ATTORNEY REVIEW."""
    )

    responses = agents["legal"].receive_and_process()
    legal_analysis = responses[0].payload if responses else "NO LEGAL ANALYSIS"
    results["legal_analysis"] = legal_analysis
    print(f"\n⚖️  Legal produced analysis ({len(legal_analysis):,} chars)")

    # ================================================================
    # STEP 3: Researcher — verify Legal's key claims
    # ================================================================
    log("STEP 3/4", "Researcher: Verify Legal's key claims and find precedents")

    agents["legal"].handoff_to(
        "researcher",
        "Verify legal analysis — find precedents and counterexamples",
        f"""Legal produced an analysis on whether our platform needs a travel agency license.

YOUR JOB: Verify or challenge the key claims. Specifically:

1. Search for any Chinese companies operating guide-matching platforms. 
   How are they structured? Do they have tourism licenses?

2. Search for enforcement actions against unlicensed online tourism platforms in China.
   Any cases in 2023-2026?

3. Is there precedent for the "information service only" / pure platform model 
   being accepted by regulators for tourism services?

4. What did the 2020 在线旅游经营服务管理暂行规定 actually change in practice?

5. Are there any industry associations or government guidance documents 
   that clarify the licensing requirements for platforms vs. agencies?

LEGAL'S KEY CLAIMS TO VERIFY:
{legal_analysis[:4000]}

Return a verification report: CONFIRMED / UNCONFIRMED / CONTRADICTED for each major claim."""
    )

    responses = agents["researcher"].receive_and_process()
    verification = responses[0].payload if responses else "NO VERIFICATION"
    results["verification"] = verification
    print(f"\n🔍 Researcher produced verification ({len(verification):,} chars)")

    # ================================================================
    # STEP 4: Legal — final GO/NO-GO memo incorporating verification
    # ================================================================
    log("STEP 4/4", "Legal: Produce final GO/NO-GO memo")

    agents["researcher"].handoff_to(
        "legal",
        "FINAL: GO/NO-GO memo for GoLocalChina business model",
        f"""Produce the FINAL GO/NO-GO decision memo for the GoLocalChina platform.

You have:
1. Your initial legal analysis
2. The Researcher's verification of your claims

PRODUCE A MEMO WITH THIS EXACT STRUCTURE:

# GO/NO-GO MEMO: GoLocalChina Platform — China Tourism Licensing

## VERDICT: [GO / CONDITIONAL GO / NO-GO]

## Executive Summary
[3-4 sentences. Can we operate? Under what conditions?]

## Licensing Requirements
[Table: License needed | How to get it | Timeline | Cost estimate]

## Recommended Business Structure
[The single best legal structure for MVP, with justification]

## Alternative Structures (Ranked)
[2-3 alternatives with GREEN/YELLOW/RED ratings]

## Critical Constraints
[Non-negotiable rules the Architect and Builder must follow]

## Risks & Mitigations
[Top 3 risks, each with a concrete mitigation]

## Immediate Next Steps
[5 specific actions the founder must take, in order]

## Appendix: Legal Citations
[Every law/regulation cited, with article numbers]

INCORPORATE THESE VERIFIED/UNVERIFIED FINDINGS:
{verification[:4000]}

YOUR EARLIER ANALYSIS:
{legal_analysis[:3000]}

This memo will be reviewed by a human lawyer, but it must be thorough enough 
to serve as their starting brief. Mark every assumption explicitly."""
    )

    responses = agents["legal"].receive_and_process()
    final_memo = responses[0].payload if responses else "NO FINAL MEMO"
    results["go_nogo_memo"] = final_memo
    print(f"\n📋 Legal produced GO/NO-GO memo ({len(final_memo):,} chars)")

    return results


def main():
    print("=" * 70)
    print("🎯 MISSION 1: VALIDATE BUSINESS MODEL LEGALITY")
    print("=" * 70)
    print()
    print("Question: Does a tourist-guide matching platform in China require")
    print("          a 旅行社业务经营许可证 (travel agency license)?")
    print()
    print("Flow: Researcher → Legal → Researcher (verify) → Legal (final memo)")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    start = time.time()
    bus = MessageBus()
    agents = create_agents(bus)

    results = mission_1(bus, agents)

    elapsed = time.time() - start

    # Save deliverables
    os.makedirs("output/mission-1", exist_ok=True)

    for key, content in results.items():
        filepath = f"output/mission-1/{key}.md"
        with open(filepath, "w") as f:
            f.write(content)
        print(f"  💾 Saved: {filepath} ({len(content):,} chars)")

    # Save the final memo as the primary deliverable
    with open("output/mission-1/DELIVERABLE.md", "w") as f:
        f.write(f"<!-- Mission 1 | Generated {time.strftime('%Y-%m-%d %H:%M:%S')} | Runtime: {elapsed:.0f}s -->\n\n")
        f.write(results.get("go_nogo_memo", "NO MEMO GENERATED"))

    # Communication log
    print(f"\n{'='*70}")
    print(f"📊 MISSION 1 COMPLETE")
    print(f"{'='*70}")
    print(f"  Messages exchanged: {len(bus.messages)}")
    print(f"  Runtime: {elapsed:.0f}s ({elapsed/60:.1f} min)")
    print(f"  Deliverables in: output/mission-1/")
    print()

    print("Message flow:")
    for msg in bus.messages:
        icons = {"request": "📨", "response": "📬", "handoff": "🔀"}
        icon = icons.get(msg.msg_type.value, "💬")
        print(f"  {icon} {msg.sender:>12} → {msg.recipient:<12} [{msg.msg_type.value:8}] {msg.subject[:55]}")

    print()
    print("Deliverables:")
    for f in sorted(os.listdir("output/mission-1")):
        size = os.path.getsize(f"output/mission-1/{f}")
        print(f"  📄 output/mission-1/{f} ({size:,} bytes)")

    # Save full mission data
    with open("output/mission-1/mission_data.json", "w") as f:
        json.dump({
            "mission": "Validate business model legality in China",
            "results": results,
            "messages": [m.to_dict() for m in bus.messages],
            "elapsed_seconds": elapsed,
        }, f, indent=2, default=str)

    print(f"\n🏁 Done. Read output/mission-1/DELIVERABLE.md for the GO/NO-GO verdict.")


if __name__ == "__main__":
    main()
