"""
Researcher Agent — Market research, competitor analysis, regulatory lookup.

Uses DuckDuckGo search as a lightweight alternative to browser-use
(which requires Python 3.11+). Loads browser-use's skill definitions
for structured research methodology.
"""
import os
from pathlib import Path
from src.core.base_agent import BaseAgent
from src.core.message_bus import MessageBus

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class ResearcherAgent(BaseAgent):
    def __init__(self, bus: MessageBus):
        super().__init__(name="Researcher", role="researcher", bus=bus)
        self._skills_cache = None

    def system_prompt(self) -> str:
        return """You are the Researcher agent for a two-sided platform connecting foreign tourists with locally certified guides in China (codename: "GoLocalChina").

Your responsibilities:
1. Market research — competitor landscape (Klook, GetYourGuide, Trip.com, Viator)
2. Regulatory research — China tourism laws, guide certification (导游证) requirements, ICP filing
3. SEO/keyword research — what tourists search for when looking for China guides
4. Guide credential verification — how 导游证 works, provincial tourism bureau systems
5. User persona research — who are the foreign tourists visiting China? demographics, needs, pain points

When you research, you:
- Cite sources explicitly
- Distinguish between verified facts and inferences
- Flag information that needs human verification
- Structure findings in actionable format for other agents

When the Architect asks you to validate an assumption, do targeted research and report back with evidence.
When Legal asks about a regulation, research the specific law and summarize key provisions.

You can perform web searches using the search tool. Always cross-reference multiple sources."""

    def skills_context(self) -> str:
        if self._skills_cache:
            return self._skills_cache

        skills = []

        # Load browser-use's agent skills
        bu_skills_dir = REPO_ROOT / "agents" / "browser-use" / "skills"
        if bu_skills_dir.exists():
            for skill_file in sorted(bu_skills_dir.glob("*.md")):
                content = skill_file.read_text()[:1500]
                skills.append(f"[Browser-Use Skill: {skill_file.stem}]\n{content}")

        # Load browser-use's AGENTS.md
        agents_md = REPO_ROOT / "agents" / "browser-use" / "AGENTS.md"
        if agents_md.exists():
            content = agents_md.read_text()[:2000]
            skills.append(f"[Browser-Use Agent Guidelines]\n{content}")

        self._skills_cache = "\n\n---\n\n".join(skills) if skills else "No browser-use skills loaded."
        return self._skills_cache

    def web_search(self, query: str, max_results: int = 5) -> str:
        """Perform a web search using DuckDuckGo."""
        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
            if not results:
                return f"No results found for: {query}"
            formatted = []
            for i, r in enumerate(results, 1):
                formatted.append(f"{i}. [{r['title']}]({r['href']})\n   {r['body']}")
            return "\n\n".join(formatted)
        except Exception as e:
            return f"Search error: {e}"

    def call_llm(self, user_msg: str, max_tokens: int = 4096) -> str:
        """Override to inject search results when research is needed."""
        # Run a few targeted searches based on the request keywords
        search_topics = []
        lower_msg = user_msg.lower()
        if "导游证" in user_msg or "guide" in lower_msg:
            search_topics.append("China tour guide license 导游证 requirements 2025")
        if "competitor" in lower_msg or "market" in lower_msg:
            search_topics.append("foreign tourist guide booking platform China competitors")
        if "payment" in lower_msg or "currency" in lower_msg:
            search_topics.append("foreign tourists payment methods China 2025")
        if not search_topics:
            search_topics.append("China tourism guide platform regulations 2025")

        # Run searches
        search_results = []
        for q in search_topics[:3]:
            result = self.web_search(q)
            search_results.append(f"[Search: {q}]\n{result}")

        # Inject search results into the user message
        enriched_msg = user_msg
        if search_results:
            enriched_msg += "\n\n--- WEB SEARCH RESULTS ---\n\n" + "\n\n".join(search_results)

        return super().call_llm(enriched_msg, max_tokens)
