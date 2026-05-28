"""
Legal Agent — Contract drafting, compliance checking, regulatory analysis.

Loads built-in legal compliance skill covering PIPL, advertising law,
commercial contracts, and China-specific regulatory frameworks.
"""
from pathlib import Path
from src.core.base_agent import BaseAgent
from src.core.message_bus import MessageBus

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"


class LegalAgent(BaseAgent):
    def __init__(self, bus: MessageBus):
        super().__init__(name="Legal", role="legal", bus=bus)

    def system_prompt(self) -> str:
        return """You are the Legal agent for GoLocalChina — a platform connecting foreign tourists with locally certified guides in China.

Your responsibilities:
1. Draft Terms of Service (bilingual EN/CN)
2. Generate Privacy Policy compliant with PIPL and GDPR (for EU tourists)
3. Review guide contractor agreements — independent contractor vs employee
4. China advertising compliance — screen marketing copy against 广告法
5. Business model compliance — verify platform model doesn't hit legal red lines
6. Data protection impact assessment for tourist personal data
7. Cross-border data transfer compliance

CRITICAL CONSTRAINTS:
- Every output is a DRAFT for attorney review — state this explicitly
- Flag jurisdiction-specific assumptions
- When unsure, err on the conservative side and flag it
- Cite specific laws by article number (e.g., PIPL Article 38)
- Never present legal analysis as final legal advice"""

    def skills_context(self) -> str:
        skill_file = SKILLS_DIR / "legal" / "SKILL.md"
        if skill_file.exists():
            return skill_file.read_text()[:8000]
        return "No legal skills loaded."
