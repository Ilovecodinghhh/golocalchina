"""
Integration Test — Run the full 4-agent workflow and verify communication.
"""
import sys
import os
import time
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.orchestrator import Orchestrator


PROJECT_BRIEF = """
Build a two-sided mobile platform connecting foreign tourists visiting China with 
locally certified tour guides (持证导游).

Key features:
- Tourists can browse guides by city, language spoken, specialty (food, history, nature)
- Guides manage their availability calendar and set their own rates
- Real-time matching and instant booking
- In-app messaging with auto-translation
- Rating/review system (both sides)
- Secure payment: tourist pays in their currency, guide receives CNY

Target cities for MVP: Beijing, Shanghai, Xi'an, Chengdu
Target tourist demographics: English-speaking tourists from US, UK, Australia, EU
"""


def main():
    print("=" * 70)
    print("🚀 CTRIP-GUIDES AGENT ORCHESTRATION TEST")
    print("=" * 70)
    print(f"\nProject: Tourist-Guide Matching Platform (China)")
    print(f"Agents: Architect, Researcher, Legal, Builder")
    print(f"Test: Full workflow — PRD → Research → Legal → Refined Spec → Build Plan")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    start = time.time()
    orch = Orchestrator()

    # Verify all agents loaded their skills
    print("📦 Skills Loading Status:")
    for name, agent in orch.agents.items():
        skills = agent.skills_context()
        skills_len = len(skills)
        status = "✅" if skills_len > 100 else "⚠️ (minimal)"
        print(f"  {status} {name:<12} — {skills_len:,} chars of skills loaded")
    print()

    # Run the full workflow
    results = orch.run_workflow(PROJECT_BRIEF)

    elapsed = time.time() - start

    # ========================================
    # COMMUNICATION REPORT
    # ========================================
    print("\n" + "=" * 70)
    print("📊 COMMUNICATION REPORT")
    print("=" * 70)
    print(f"\nTotal messages on bus: {len(orch.bus.messages)}")
    print(f"Total time: {elapsed:.1f}s")
    print()

    # Message flow diagram
    print("Message Flow:")
    for msg in orch.bus.messages:
        arrow = "→"
        icon = {"request": "📨", "response": "📬", "handoff": "🔀", "broadcast": "📢"}.get(msg.msg_type.value, "💬")
        print(f"  {icon} {msg.sender:<12} {arrow} {msg.recipient:<12} [{msg.msg_type.value}] {msg.subject[:50]}")
    print()

    # Agent status
    print("Agent Status:")
    for name, agent in orch.agents.items():
        s = agent.status()
        print(f"  {name:<12} — {s['messages_in_history']} LLM turns, {s['work_products']} outputs")
    print()

    # ========================================
    # WORK PRODUCTS SUMMARY
    # ========================================
    print("=" * 70)
    print("📄 WORK PRODUCTS")
    print("=" * 70)

    for key, content in results.items():
        print(f"\n{'─'*40}")
        print(f"📎 {key.upper()} ({len(content)} chars)")
        print(f"{'─'*40}")
        # Print first 500 chars of each
        print(content[:500])
        if len(content) > 500:
            print(f"\n  [...truncated, full output: {len(content)} chars...]")

    # ========================================
    # PASS/FAIL
    # ========================================
    print("\n" + "=" * 70)
    print("✅ TEST RESULTS")
    print("=" * 70)

    tests = [
        ("Architect produced PRD", len(results.get("prd", "")) > 200),
        ("Researcher produced findings", len(results.get("research", "")) > 200),
        ("Legal produced compliance review", len(results.get("legal_review", "")) > 200),
        ("Architect refined spec", len(results.get("final_spec", "")) > 200),
        ("Builder produced implementation plan", len(results.get("implementation_plan", "")) > 200),
        ("Messages flowed between agents", len(orch.bus.messages) >= 8),
        ("All agents processed work", all(a.status()["work_products"] > 0 for a in orch.agents.values())),
    ]

    all_pass = True
    for test_name, passed in tests:
        icon = "✅" if passed else "❌"
        print(f"  {icon} {test_name}")
        if not passed:
            all_pass = False

    print()
    if all_pass:
        print("🎉 ALL TESTS PASSED — Agents communicate and produce work products successfully!")
    else:
        print("⚠️  Some tests failed — check the output above.")

    print(f"\nTotal runtime: {elapsed:.1f}s")

    # Save full results
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_results.json")
    with open(output_path, "w") as f:
        json.dump({
            "results": results,
            "messages": [m.to_dict() for m in orch.bus.messages],
            "elapsed_seconds": elapsed,
            "tests_passed": all_pass,
        }, f, indent=2, default=str)
    print(f"Full results saved to: {output_path}")


if __name__ == "__main__":
    main()
