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

This tests the full communication loop.
"""
import json
import time
from src.core.message_bus import MessageBus, Message, MessageType, AgentRole
from src.agents.architect import ArchitectAgent
from src.agents.researcher import ResearcherAgent
from src.agents.legal import LegalAgent
from src.agents.builder import BuilderAgent


class Orchestrator:
    """Coordinates sub-agents through structured workflows."""

    def __init__(self):
        self.bus = MessageBus()
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

        # ========================================
        # STEP 1: Brief → Architect (write PRD)
        # ========================================
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

Keep it under 800 words. Be specific and actionable — the Builder agent will implement from this."""
        ))

        responses = self.architect.receive_and_process()
        prd = responses[0].payload if responses else "NO PRD GENERATED"
        results["prd"] = prd
        print(f"\n📋 Architect produced PRD ({len(prd)} chars)")

        # ========================================
        # STEP 2: PRD → Researcher (validate assumptions)
        # ========================================
        self.log("STEP 2", "Sending PRD to Researcher for market validation")

        self.architect.handoff_to(
            "researcher",
            "Validate PRD assumptions — market & regulatory",
            f"""The Architect produced this PRD. Please validate the key assumptions by researching:

1. Are there existing competitors doing exactly this in China? What's their model?
2. What are the actual 导游证 (guide license) requirements — who issues them, what's the process?
3. What payment methods do foreign tourists in China actually use?

PRD:
{prd[:2000]}

Return a structured findings report. Flag anything in the PRD that's wrong or needs correction."""
        )

        responses = self.researcher.receive_and_process()
        research = responses[0].payload if responses else "NO RESEARCH GENERATED"
        results["research"] = research
        print(f"\n🔍 Researcher produced findings ({len(research)} chars)")

        # ========================================
        # STEP 3: PRD → Legal (compliance review)
        # ========================================
        self.log("STEP 3", "Sending PRD to Legal for compliance review")

        self.architect.handoff_to(
            "legal",
            "Compliance review of platform PRD",
            f"""Review this PRD for legal and compliance issues. Specifically check:

1. PIPL compliance — what data handling constraints affect the data model?
2. China advertising law — any marketing claims in the PRD that violate 广告法?
3. Business model legality — does a tourist-guide matching platform need a 旅行社业务经营许可证?
4. Cross-border data — tourist data (EU/US citizens) being processed in China
5. Guide classification — independent contractor vs employee risk

PRD:
{prd[:2000]}

Return a compliance checklist with GREEN/YELLOW/RED ratings per item."""
        )

        responses = self.legal.receive_and_process()
        legal_review = responses[0].payload if responses else "NO LEGAL REVIEW GENERATED"
        results["legal_review"] = legal_review
        print(f"\n⚖️  Legal produced compliance review ({len(legal_review)} chars)")

        # ========================================
        # STEP 4: Feed research + legal back to Architect for refinement
        # ========================================
        self.log("STEP 4", "Feeding research & legal findings back to Architect")

        self.bus.post(Message(
            sender="orchestrator",
            recipient="architect",
            msg_type=MessageType.REQUEST,
            subject="Refine PRD based on research & legal findings",
            payload=f"""Your PRD received feedback from two agents. Produce a REVISED technical spec.

RESEARCHER FINDINGS:
{research[:1500]}

LEGAL COMPLIANCE REVIEW:
{legal_review[:1500]}

Produce a final Technical Specification that:
1. Incorporates the researcher's market corrections
2. Addresses all RED and YELLOW legal flags
3. Defines the database schema (table names, key columns)
4. Lists the top 5 API endpoints with request/response shapes
5. Notes any constraints the Builder must follow

Keep it under 600 words. Make it directly implementable."""
        ))

        responses = self.architect.receive_and_process()
        final_spec = responses[0].payload if responses else "NO FINAL SPEC GENERATED"
        results["final_spec"] = final_spec
        print(f"\n📐 Architect produced final spec ({len(final_spec)} chars)")

        # ========================================
        # STEP 5: Final spec → Builder (implementation plan)
        # ========================================
        self.log("STEP 5", "Handing final spec to Builder for implementation plan")

        self.architect.handoff_to(
            "builder",
            "Implement GoLocalChina MVP from spec",
            f"""Here is the final technical specification. Produce an implementation plan:

{final_spec[:2500]}

Produce:
1. Project file/folder structure
2. Database migration SQL (CREATE TABLE statements)
3. One complete API endpoint implementation (the most critical one)
4. A brief explanation of your tech stack choices

This is the implementation plan — not the full codebase. Show enough to prove the spec is buildable."""
        )

        responses = self.builder.receive_and_process()
        impl_plan = responses[0].payload if responses else "NO IMPLEMENTATION PLAN GENERATED"
        results["implementation_plan"] = impl_plan
        print(f"\n🔨 Builder produced implementation plan ({len(impl_plan)} chars)")

        # ========================================
        # SUMMARY
        # ========================================
        self.log("COMPLETE", f"All 5 steps finished. {len(self.bus.messages)} messages exchanged.")

        return results
