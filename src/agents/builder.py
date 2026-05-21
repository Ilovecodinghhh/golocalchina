"""
Builder Agent — Writes all code: frontend, backend, infra, DevOps.

This agent receives specs from Architect and produces implementable code.
It represents the Claude Code coding capability.
"""
import os
from pathlib import Path
from src.core.base_agent import BaseAgent
from src.core.message_bus import MessageBus

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class BuilderAgent(BaseAgent):
    def __init__(self, bus: MessageBus):
        super().__init__(name="Builder", role="builder", bus=bus)
        self._skills_cache = None

    def system_prompt(self) -> str:
        return """You are the Builder agent for a two-sided platform connecting foreign tourists with locally certified guides in China (codename: "Ctrip-Guides").

Your responsibilities:
1. Implement frontend (React Native / Next.js) from Architect's specs
2. Build backend API (FastAPI / Python) with matching algorithm, booking, payments
3. Set up database schema (PostgreSQL) from Architect's data models
4. Write Docker/docker-compose configs for local development
5. Create CI/CD pipeline configs
6. Implement i18n infrastructure
7. Write tests for all critical paths

You follow these principles:
- Mobile-first responsive design
- API-first architecture (OpenAPI specs)
- Type-safe code with full type hints
- Comprehensive error handling
- Security by default (OWASP top 10)
- i18n from day 1 (not bolted on)

When you receive a spec from Architect:
1. Acknowledge what you'll build
2. Identify any ambiguities and ask Architect to clarify
3. Produce the code with clear file structure
4. Note any Legal constraints that affect implementation (e.g., data residency)

When Legal flags compliance requirements, incorporate them into the implementation."""

    def skills_context(self) -> str:
        if self._skills_cache:
            return self._skills_cache

        skills = []

        # Load MetaGPT's Engineer role prompt for coding best practices
        eng_prompt = REPO_ROOT / "agents" / "metagpt" / "metagpt" / "prompts" / "di" / "engineer2.py"
        if eng_prompt.exists():
            content = eng_prompt.read_text()[:2000]
            skills.append(f"[MetaGPT Engineer Prompt Reference]\n{content}")

        # Load MetaGPT's code review action
        review_path = REPO_ROOT / "agents" / "metagpt" / "metagpt" / "actions" / "write_code.py"
        if review_path.exists():
            content = review_path.read_text()[:2000]
            skills.append(f"[MetaGPT Code Writing Reference]\n{content}")

        self._skills_cache = "\n\n---\n\n".join(skills) if skills else "No builder skills loaded."
        return self._skills_cache
