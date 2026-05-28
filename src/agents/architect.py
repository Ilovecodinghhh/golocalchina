"""
Architect Agent — Product specs, system design, API contracts.

Loads built-in architecture skill for PRD writing and system design patterns.
"""
from pathlib import Path
from src.core.base_agent import BaseAgent
from src.core.message_bus import MessageBus

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"


class ArchitectAgent(BaseAgent):
    def __init__(self, bus: MessageBus):
        super().__init__(name="Architect", role="architect", bus=bus)

    def system_prompt(self) -> str:
        return """You are the Architect agent for GoLocalChina — a platform connecting foreign tourists with locally certified guides in China.

Your responsibilities:
1. Write Product Requirement Documents (PRDs) from high-level ideas
2. Design system architecture (database schema, API contracts, service boundaries)
3. Define data models and matching algorithms (tourist ↔ guide)
4. Create wireframe descriptions and user flow specifications
5. Break down work into implementable tasks for the Builder agent

Design thinking:
- Two-sided marketplace dynamics (supply: guides, demand: tourists)
- Cross-border concerns (i18n, multi-currency, timezone)
- China-specific infra (ICP, GFW, domestic hosting)
- Mobile-first design (tourists are traveling)

When handing off to Builder, be specific: include API endpoint signatures, database table definitions, and component hierarchies."""

    def skills_context(self) -> str:
        skill_file = SKILLS_DIR / "architecture" / "SKILL.md"
        if skill_file.exists():
            return skill_file.read_text()[:8000]
        return "No architecture skills loaded."
