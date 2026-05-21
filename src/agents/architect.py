"""
Architect Agent — Product specs, system design, API contracts.

Loads MetaGPT's ProductManager + Architect role prompts as skills context.
"""
import os
from pathlib import Path
from src.core.base_agent import BaseAgent
from src.core.message_bus import MessageBus


REPO_ROOT = Path(__file__).resolve().parent.parent.parent

class ArchitectAgent(BaseAgent):
    def __init__(self, bus: MessageBus):
        super().__init__(name="Architect", role="architect", bus=bus)
        self._skills_cache = None

    def system_prompt(self) -> str:
        return """You are the Architect agent for a two-sided platform connecting foreign tourists with locally certified guides in China (codename: "Ctrip-Guides").

Your responsibilities:
1. Write Product Requirement Documents (PRDs) from high-level ideas
2. Design system architecture (database schema, API contracts, service boundaries)
3. Define data models and matching algorithms (tourist ↔ guide)
4. Create wireframe descriptions and user flow specifications
5. Break down work into implementable tasks for the Builder agent

You think in terms of:
- Two-sided marketplace dynamics (supply: guides, demand: tourists)
- Cross-border concerns (i18n, multi-currency, timezone)
- China-specific infra (ICP, GFW, domestic hosting)
- Mobile-first design (tourists are traveling)

When you receive a request, produce structured, actionable specs that a Builder agent can implement directly. Use markdown with clear sections.

When handing off to Builder, be specific: include API endpoint signatures, database table definitions, and component hierarchies."""

    def skills_context(self) -> str:
        if self._skills_cache:
            return self._skills_cache

        skills = []

        # Load MetaGPT's ProductManager prompt
        pm_prompt_path = REPO_ROOT / "agents" / "metagpt" / "metagpt" / "prompts" / "product_manager.py"
        if pm_prompt_path.exists():
            content = pm_prompt_path.read_text()[:2000]
            skills.append(f"[MetaGPT PM Prompt Reference]\n{content}")

        # Load MetaGPT's Architect prompt
        arch_prompt_path = REPO_ROOT / "agents" / "metagpt" / "metagpt" / "prompts" / "di" / "architect.py"
        if arch_prompt_path.exists():
            content = arch_prompt_path.read_text()[:2000]
            skills.append(f"[MetaGPT Architect Prompt Reference]\n{content}")

        # Load MetaGPT's WritePRD action
        prd_path = REPO_ROOT / "agents" / "metagpt" / "metagpt" / "actions" / "write_prd.py"
        if prd_path.exists():
            content = prd_path.read_text()[:2000]
            skills.append(f"[MetaGPT PRD Writing Reference]\n{content}")

        self._skills_cache = "\n\n---\n\n".join(skills) if skills else "No MetaGPT skills loaded."
        return self._skills_cache
