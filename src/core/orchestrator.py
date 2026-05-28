"""
Orchestrator — Coordinates the 4 agents through a structured workflow.

Workflow:
1. Orchestrator sends initial brief to Architect
2. Architect produces PRD → hands off to Researcher for validation
3. Researcher validates assumptions → returns findings to Architect
4. Architect refines specs → sends to Legal for compliance review
5. Legal reviews → flags constraints → returns to Architect
6. Architect produces final spec → hands off to Builder
7. Builder produces implementation plan

Messages are persisted to SQLite for audit and recovery.
"""
import os
import time
from src.core.message_bus import MessageBus, Message, MessageType, AgentRole
from src.agents.architect import ArchitectAgent
from src.agents.researcher import ResearcherAgent
from src.agents.legal import LegalAgent
from src.agents.builder import BuilderAgent


class Orchestrator:
    """Coordinates sub-agents through structured workflows."""

    def __init__(self, db_path: str | None = None):
        # Use persistent message bus (SQLite-backed)
        if db_path is None:
            db_path = os.environ.get("MESSAGE_BUS_DB", "message_bus.db")
        self.bus = MessageBus(db_path=db_path)
        self.architect = ArchitectAgent(self.bus)
        self.researcher = ResearcherAgent(self.bus)
        self.legal = LegalAgent(self.bus)
        self.builder = BuilderAgent(self.bus)
        self.agents = {
            "architect": self.architect,
            "researcher": self.researcher,
            "legal": self.legal,
            "builder": self.builder,
        }

    def log(self, step: str, detail: str = ""):
        timestamp = time.strftime("%H:%M:%S")
        print(f"\n{'='*70}")
        print(f"[{timestamp}] ORCHESTRATOR — {step}")
        if detail:
            print(f"  {detail}")
        print(f"{'='*70}")

    def run_workflow(self, project_brief: str) -> dict:
        """Run the full agent coordination workflow."""
        results = {}

        # STEP 1: Brief → Architect (write PRD)
        self.log("STEP 1", "Sending project brief to Architect for PRD")

        self.bus.post(Message(
            sender="orchestrator",
            recipient="architect",
            msg_type=MessageType.REQUEST,
            subject="Write PRD for GoLocalChina platform",
            payload=f"""Write a concise Product Requirement Document for this platform:

{project_brief}

Focus on:
- Core user stories (tourist booking a guide, guide managing availability)
- Data model (key entities and relationships)
- API endpoints (top 5 critical ones)
- MVP scope (what's in v1 vs later)

Keep it under 800 words. Be specific and actionable."""
        ))

        responses = self.architect.receive_and_process()
        prd = responses[0].payload if responses else "NO PRD GENERATED"
        results["prd"] = prd
        print(f"\nArchitect produced PRD ({len(prd)} chars)")

        # STEP 2: PRD → Researcher (validate assumptions)
        self.log("STEP 2", "Sending PRD to Researcher for market validation")

        self.architect.handoff_to(
            "researcher",
            "Validate PRD assumptions",
            f"""Validate the key assumptions in this PRD:

1. Are there existing competitors doing exactly this in China?
2. What are the actual guide license (导游证) requirements?
3. What payment methods do foreign tourists in China actually use?

PRD:
{prd[:2000]}

Return structured findings. Flag anything wrong or needing correction."""
        )

        responses = self.researcher.receive_and_process()
        research = responses[0].payload if responses else "NO RESEARCH GENERATED"
        results["research"] = research
        print(f"\nResearcher produced findings ({len(research)} chars)")

        # STEP 3: PRD → Legal (compliance review)
        self.log("STEP 3", "Sending PRD to Legal for compliance review")

        self.architect.handoff_to(
            "legal",
            "Compliance review of platform PRD",
            f"""Review this PRD for legal and compliance issues:

1. PIPL compliance — data handling constraints
2. China advertising law — any claims violating 广告法?
3. Business model legality — does this need 旅行社业务经营许可证?
4. Cross-border data — tourist data processed in China
5. Guide classification — contractor vs employee risk

PRD:
{prd[:2000]}

Return compliance checklist with GREEN/YELLOW/RED ratings."""
        )

        responses = self.legal.receive_and_process()
        legal_review = responses[0].payload if responses else "NO LEGAL REVIEW GENERATED"
        results["legal_review"] = legal_review
        print(f"\nLegal produced compliance review ({len(legal_review)} chars)")

        # STEP 4: Feed research + legal back to Architect
        self.log("STEP 4", "Feeding research & legal findings back to Architect")

        self.bus.post(Message(
            sender="orchestrator",
            recipient="architect",
            msg_type=MessageType.REQUEST,
            subject="Refine PRD based on research & legal findings",
            payload=f"""Produce a REVISED technical spec based on this feedback:

RESEARCHER FINDINGS:
{research[:1500]}

LEGAL COMPLIANCE REVIEW:
{legal_review[:1500]}

Produce a final Technical Specification that:
1. Incorporates market corrections
2. Addresses all RED and YELLOW legal flags
3. Defines database schema (table names, key columns)
4. Lists top 5 API endpoints with request/response shapes
5. Notes constraints the Builder must follow

Keep it under 600 words. Make it directly implementable."""
        ))

        responses = self.architect.receive_and_process()
        final_spec = responses[0].payload if responses else "NO FINAL SPEC GENERATED"
        results["final_spec"] = final_spec
        print(f"\nArchitect produced final spec ({len(final_spec)} chars)")

        # STEP 5: Final spec → Builder (implementation plan)
        self.log("STEP 5", "Handing final spec to Builder for implementation plan")

        self.architect.handoff_to(
            "builder",
            "Implement GoLocalChina MVP from spec",
            f"""Produce an implementation plan from this spec:

{final_spec[:2500]}

Produce:
1. Project file/folder structure
2. Database migration SQL (CREATE TABLE statements)
3. One complete API endpoint implementation (the most critical one)
4. Brief explanation of tech stack choices"""
        )

        responses = self.builder.receive_and_process()
        impl_plan = responses[0].payload if responses else "NO IMPLEMENTATION PLAN GENERATED"
        results["implementation_plan"] = impl_plan
        print(f"\nBuilder produced implementation plan ({len(impl_plan)} chars)")

        # SUMMARY
        msg_count = self.bus.get_stats()["total_messages"]
        self.log("COMPLETE", f"All 5 steps finished. {msg_count} messages exchanged.")

        return results
