"""
Researcher Agent — Market research, competitor analysis, regulatory lookup.

Uses DuckDuckGo search for web research.
Loads built-in research methodology skill.
"""
from pathlib import Path
from src.core.base_agent import BaseAgent
from src.core.message_bus import MessageBus

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"


class ResearcherAgent(BaseAgent):
    def __init__(self, bus: MessageBus):
        super().__init__(name="Researcher", role="researcher", bus=bus)

    def system_prompt(self) -> str:
        return """You are the Researcher agent for GoLocalChina — a platform connecting foreign tourists with locally certified guides in China.

Your responsibilities:
1. Market research — competitor landscape (Klook, GetYourGuide, Trip.com, Viator)
2. Regulatory research — China tourism laws, guide certification (导游证), ICP filing
3. SEO/keyword research — what tourists search for
4. Guide credential verification — how 导游证 works, provincial tourism bureau systems
5. User persona research — foreign tourist demographics, needs, pain points

Research principles:
- Cite sources explicitly with URLs
- Distinguish verified facts from inferences
- Flag information needing human verification
- Structure findings in actionable format for other agents
- Cross-reference multiple sources before stating facts"""

    def skills_context(self) -> str:
        skill_file = SKILLS_DIR / "research" / "SKILL.md"
        if skill_file.exists():
            return skill_file.read_text()[:8000]
        return "No research skills loaded."

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

        search_results = []
        for q in search_topics[:3]:
            result = self.web_search(q)
            search_results.append(f"[Search: {q}]\n{result}")

        enriched_msg = user_msg
        if search_results:
            enriched_msg += "\n\n--- WEB SEARCH RESULTS ---\n\n" + "\n\n".join(search_results)

        return super().call_llm(enriched_msg, max_tokens)
