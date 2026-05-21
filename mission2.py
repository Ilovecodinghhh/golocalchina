"""
Mission 2: Produce the MVP Technical Spec
Path B (pure tech platform, no travel agency license) — small scale MVP.

FLOW: Architect → Researcher → Legal → Architect (final spec)
DELIVERABLE: Complete technical specification ready for Builder
"""
import sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.message_bus import MessageBus, Message, MessageType
from src.agents.architect import ArchitectAgent
from src.agents.researcher import ResearcherAgent
from src.agents.legal import LegalAgent


def main():
    print("=" * 70)
    print("🎯 MISSION 2: MVP TECHNICAL SPEC (Path B — Pure Platform)")
    print("=" * 70)
    print()
    print("Founder decision: Path B — operate as pure tech/information platform.")
    print("Scale: Small. 4 cities, <50 guides, prove the concept before licensing.")
    print("Flow: Architect → Researcher (tech validation) → Legal (constraints) → Architect (final)")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    start = time.time()
    bus = MessageBus()
    architect = ArchitectAgent(bus)
    researcher = ResearcherAgent(bus)
    legal = LegalAgent(bus)

    results = {}

    # Load Mission 1 findings so agents have context
    m1_legal = ""
    m1_path = "output/mission-1/legal_analysis.md"
    if os.path.exists(m1_path):
        with open(m1_path) as f:
            m1_legal = f.read()[:3000]

    log = lambda step, detail="": print(f"\n{'='*70}\n[{time.strftime('%H:%M:%S')}] MISSION 2 — {step}\n  {detail}\n{'='*70}")

    # ================================================================
    # STEP 1: Architect — Draft full technical spec
    # ================================================================
    log("STEP 1/4", "Architect: Draft MVP technical specification")

    bus.post(Message(
        sender="mission",
        recipient="architect",
        msg_type=MessageType.REQUEST,
        subject="Write MVP Technical Specification — Path B pure platform",
        payload=f"""Write the complete MVP Technical Specification for Ctrip-Guides.

FOUNDER DECISIONS (non-negotiable):
- Path B: Pure tech/information platform. NO travel agency license for now.
- We position as an "information matching service" (信息技术服务), not a travel agency.
- Guides are independent. We do NOT organize tours, bundle transport, or set prices.
- Small scale: Beijing, Shanghai, Xi'an, Chengdu. Target: 50 guides, 200 bookings/month.
- Commission model: 12% service fee (called "platform service fee", not "tour commission").
- Payment: Stripe for foreign cards → platform holds briefly → Alipay/WeChat Pay payout to guide.
- Mobile web first (PWA), native app later.

LEGAL CONTEXT FROM MISSION 1 (Path B constraints):
{m1_legal[:2000]}

PRODUCE THE FULL SPEC WITH THESE SECTIONS:

1. **System Architecture Overview**
   - Service diagram (what talks to what)
   - Tech stack choices with justification
   - Hosting strategy (China + international)

2. **Data Model**
   - All tables with columns, types, constraints
   - Relationships and indexes
   - Data residency rules (what stays in China, what doesn't)

3. **API Specification**
   - Every endpoint for MVP (method, path, request/response schemas)
   - Auth strategy (JWT, session, etc.)
   - Rate limiting and error handling patterns

4. **Core Algorithms**
   - Guide search and ranking
   - Availability matching
   - FX rate calculation and quoting

5. **Payment Flow**
   - Step-by-step: tourist card charge → platform hold → guide payout
   - Refund/cancellation flow
   - Fee calculation (show tourist and guide what they each pay/receive)

6. **i18n Architecture**
   - Supported languages for MVP
   - Auto-translation strategy for chat
   - Content management (guide bios, reviews)

7. **Security & Compliance Checklist**
   - Auth, encryption, data handling
   - Path B legal constraints baked into the tech

8. **MVP Milestone Plan**
   - 4-week sprint breakdown
   - What ships each week
   - Definition of "done" for MVP launch

Be extremely specific. Include actual table DDL, actual endpoint signatures, 
actual component names. The Builder agent will implement directly from this."""
    ))

    responses = architect.receive_and_process()
    draft_spec = responses[0].payload if responses else "FAILED"
    results["draft_spec"] = draft_spec
    print(f"\n📐 Architect produced draft spec ({len(draft_spec):,} chars)")

    # ================================================================
    # STEP 2: Researcher — Validate tech choices
    # ================================================================
    log("STEP 2/4", "Researcher: Validate tech stack and China infra choices")

    architect.handoff_to(
        "researcher",
        "Validate tech choices for China deployment",
        f"""The Architect drafted a technical spec. Validate these specific choices:

1. **Payment providers**: Can Stripe actually process foreign cards for a China-based platform?
   What about Airwallex, Adyen, PingPong? Which is best for our use case (foreign card → CNY)?

2. **Hosting in China**: Aliyun vs Tencent Cloud vs Huawei Cloud — which is best for a 
   small startup? What does ICP filing actually require and how long does it take?

3. **Translation APIs**: Tencent Cloud MT vs DeepL vs Google Translate — which works 
   inside the GFW? Latency and cost comparison for chat translation.

4. **Maps**: Gaode/Amap vs Baidu Maps vs Tencent Maps — which has the best English API?
   Can we use Mapbox or Google Maps at all inside China?

5. **Real-time chat**: WebSocket options that work well behind GFW. 
   Any China-specific gotchas with real-time connections?

ARCHITECT'S TECH CHOICES TO VALIDATE:
{draft_spec[:3000]}

Return a validation report: CONFIRMED / BETTER ALTERNATIVE for each choice."""
    )

    responses = researcher.receive_and_process()
    tech_validation = responses[0].payload if responses else "FAILED"
    results["tech_validation"] = tech_validation
    print(f"\n🔍 Researcher produced tech validation ({len(tech_validation):,} chars)")

    # ================================================================
    # STEP 3: Legal — Stamp Path B constraints onto spec
    # ================================================================
    log("STEP 3/4", "Legal: Review spec for Path B compliance constraints")

    architect.handoff_to(
        "legal",
        "Review technical spec — stamp Path B legal constraints",
        f"""Review this technical spec and ensure it STRICTLY adheres to Path B 
(pure information platform, no travel agency license).

CRITICAL: The spec must NOT contain any features that could be construed as 
"organizing or arranging tours" under 旅行社条例 Art. 2. 

REVIEW FOR:
1. **Language/framing**: Any feature names, UI copy, or API fields that imply 
   we are a travel agency? (e.g., "book a tour" → should be "connect with a guide")
   
2. **Payment flow**: Does the platform holding funds briefly create custody risk?
   Does the fee structure look like a travel agency commission?

3. **Data model**: Any fields that imply we're organizing tours rather than 
   just connecting people? (e.g., "tour_package", "itinerary" → problematic)

4. **Guide relationship**: Does anything in the spec make guides look like employees?
   Independent contractor classification safeguards?

5. **PIPL minimum**: What personal data handling requirements must be in the spec?
   Consent flows, data deletion, cross-border transfer.

6. **MCT Order No.4 floor**: The 8 obligations from Mission 1 — are they all 
   reflected in this spec?

SPEC TO REVIEW:
{draft_spec[:4000]}

Return: A list of REQUIRED CHANGES (must fix) and RECOMMENDED CHANGES (should fix).
For each, give the exact spec section and what to change it to."""
    )

    responses = legal.receive_and_process()
    legal_constraints = responses[0].payload if responses else "FAILED"
    results["legal_constraints"] = legal_constraints
    print(f"\n⚖️  Legal produced constraints ({len(legal_constraints):,} chars)")

    # ================================================================
    # STEP 4: Architect — Produce final spec incorporating all feedback
    # ================================================================
    log("STEP 4/4", "Architect: Final spec incorporating tech validation + legal constraints")

    bus.post(Message(
        sender="mission",
        recipient="architect",
        msg_type=MessageType.REQUEST,
        subject="FINAL: Produce definitive MVP technical spec",
        payload=f"""Produce the FINAL MVP Technical Specification incorporating:

1. Researcher's tech validation (use confirmed choices, swap to better alternatives)
2. Legal's required changes (ALL must be incorporated)
3. Legal's recommended changes (incorporate unless they break the architecture)

RESEARCHER TECH VALIDATION:
{tech_validation[:3000]}

LEGAL REQUIRED/RECOMMENDED CHANGES:
{legal_constraints[:3000]}

YOUR ORIGINAL DRAFT (for reference):
{draft_spec[:2000]}

OUTPUT THE COMPLETE FINAL SPEC. This is the definitive document the Builder will implement from.
Include a "Changes from Draft" section at the top summarizing what changed and why.
Every table, endpoint, and component must be present and final."""
    ))

    responses = architect.receive_and_process()
    final_spec = responses[0].payload if responses else "FAILED"
    results["final_spec"] = final_spec
    print(f"\n📐 Architect produced FINAL spec ({len(final_spec):,} chars)")

    elapsed = time.time() - start

    # Save deliverables
    os.makedirs("output/mission-2", exist_ok=True)

    for key, content in results.items():
        filepath = f"output/mission-2/{key}.md"
        with open(filepath, "w") as f:
            f.write(content)

    with open("output/mission-2/DELIVERABLE.md", "w") as f:
        f.write(f"<!-- Mission 2 | {time.strftime('%Y-%m-%d %H:%M:%S')} | {elapsed:.0f}s | Path B -->\n\n")
        f.write(results.get("final_spec", "FAILED"))

    with open("output/mission-2/mission_data.json", "w") as f:
        json.dump({
            "mission": "MVP Technical Spec (Path B)",
            "results": results,
            "messages": [m.to_dict() for m in bus.messages],
            "elapsed_seconds": elapsed,
        }, f, indent=2, default=str)

    # Report
    print(f"\n{'='*70}")
    print(f"📊 MISSION 2 COMPLETE")
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
    for fn in sorted(os.listdir("output/mission-2")):
        size = os.path.getsize(f"output/mission-2/{fn}")
        print(f"  📄 output/mission-2/{fn} ({size:,} bytes)")
    print(f"\n🏁 Done. Read output/mission-2/DELIVERABLE.md for the final spec.")


if __name__ == "__main__":
    main()
