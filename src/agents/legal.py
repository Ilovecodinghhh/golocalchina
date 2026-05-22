"""
Legal Agent — Contract drafting, compliance checking, regulatory analysis.

Loads skills from:
- anthropics/claude-for-legal (privacy-legal, commercial-legal, product-legal)
- kuanghs/agent-skills (cn-business-compliance, cn-advertising-compliance, cn-ecommerce-compliance)
"""
import os
from pathlib import Path
from src.core.base_agent import BaseAgent
from src.core.message_bus import MessageBus

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class LegalAgent(BaseAgent):
    def __init__(self, bus: MessageBus):
        super().__init__(name="Legal", role="legal", bus=bus)
        self._skills_cache = None

    def system_prompt(self) -> str:
        return """You are the Legal agent for a two-sided platform connecting foreign tourists with locally certified guides in China (codename: "GoLocalChina").

Your responsibilities:
1. Draft Terms of Service for the platform (bilingual EN/CN)
2. Generate Privacy Policy compliant with China's PIPL and GDPR (for EU tourists)
3. Review guide contractor agreements — classify as independent contractor vs employee
4. China advertising compliance — screen all marketing copy against 广告法
5. Business model compliance — verify the platform model doesn't hit China legal red lines
6. Data protection impact assessment for tourist personal data handling
7. Cross-border data transfer compliance (tourist data leaving/entering China)

CRITICAL CONSTRAINTS:
- Every output is a DRAFT for attorney review — state this explicitly
- Flag jurisdiction-specific assumptions
- When unsure about a provision, err on the conservative side and flag it
- Cite specific laws by article number when possible (e.g., PIPL Article 38)
- Never present legal analysis as final legal advice

You have loaded skills from:
- anthropics/claude-for-legal: privacy-legal, commercial-legal, product-legal plugins
- China compliance skills: business compliance, advertising compliance, e-commerce compliance

When the Architect asks about legal constraints, provide specific requirements that affect system design.
When the Researcher provides regulatory findings, analyze them and produce actionable compliance checklists."""

    def skills_context(self) -> str:
        if self._skills_cache:
            return self._skills_cache

        skills = []

        # --- claude-for-legal: load only the most relevant skills (trimmed) ---

        # Privacy: PIA generation and use-case triage (most relevant for PIPL)
        for skill_name in ["pia-generation", "use-case-triage", "dpa-review"]:
            skill_md = REPO_ROOT / "agents" / "claude-for-legal" / "privacy-legal" / "skills" / skill_name / "SKILL.md"
            if skill_md.exists():
                content = skill_md.read_text()[:800]
                skills.append(f"[Privacy: {skill_name}]\n{content}")

        # Commercial: review + vendor-agreement-review
        for skill_name in ["review", "vendor-agreement-review"]:
            skill_md = REPO_ROOT / "agents" / "claude-for-legal" / "commercial-legal" / "skills" / skill_name / "SKILL.md"
            if skill_md.exists():
                content = skill_md.read_text()[:800]
                skills.append(f"[Commercial: {skill_name}]\n{content}")

        # Product: launch-review
        skill_md = REPO_ROOT / "agents" / "claude-for-legal" / "product-legal" / "skills" / "launch-review" / "SKILL.md"
        if skill_md.exists():
            content = skill_md.read_text()[:800]
            skills.append(f"[Product: launch-review]\n{content}")

        # --- China compliance skills (essential — load SKILL.md only, no refs) ---
        cn_skills = [
            ("cn-business-compliance-check", "China Business Compliance"),
            ("cn-advertising-compliance", "China Advertising Compliance"),
        ]
        for dirname, label in cn_skills:
            skill_md = REPO_ROOT / "agents" / "china-compliance" / dirname / "SKILL.md"
            if skill_md.exists():
                content = skill_md.read_text()[:1200]
                skills.append(f"[{label}]\n{content}")

        self._skills_cache = "\n\n---\n\n".join(skills) if skills else "No legal skills loaded."
        return self._skills_cache
