"""
Base Agent — Abstract agent class all sub-agents inherit from.

Uses pluggable LLMProvider (Anthropic/OpenAI/Mock) with:
- Retry with exponential backoff
- Graceful degradation on persistent failures
- Proper system/user message separation (no duplication)
"""
from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod
from typing import Optional

from src.core.llm_provider import LLMProvider, LLMResponse, get_provider
from src.core.message_bus import MessageBus, Message, MessageType

logger = logging.getLogger(__name__)


class AgentError(Exception):
    """Raised when an agent encounters an unrecoverable error."""
    pass


class BaseAgent(ABC):
    """Base class for all sub-agents."""

    # Retry configuration
    MAX_RETRIES = 3
    RETRY_BASE_DELAY = 1.0  # seconds
    RETRY_MAX_DELAY = 30.0

    def __init__(
        self,
        name: str,
        role: str,
        bus: MessageBus,
        llm_provider: Optional[LLMProvider] = None,
    ):
        self.name = name
        self.role = role
        self.bus = bus
        self.conversation_history: list[dict] = []
        self.work_products: list[dict] = []
        self.llm: LLMProvider = llm_provider or get_provider()
        self._consecutive_failures = 0

    @abstractmethod
    def system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        pass

    @abstractmethod
    def skills_context(self) -> str:
        """Return loaded skills/knowledge context for this agent."""
        pass

    def call_llm(
        self,
        user_msg: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        """Make an LLM call with retry and graceful degradation.

        Fixes:
        - System prompt passed ONLY as system parameter (not duplicated in user msg)
        - Conversation history passed as proper message list (not string concat)
        - Retry with exponential backoff on transient failures
        - Degradation message on persistent failures
        """
        # Build system prompt (skills context appended here, NOT in user message)
        system = self.system_prompt()
        skills = self.skills_context()
        if skills and skills != "No skills loaded.":
            system += f"\n\n--- LOADED SKILLS ---\n{skills[:8000]}"

        # Build proper message list from conversation history
        messages = []
        for entry in self.conversation_history[-6:]:  # Last 3 exchanges
            messages.append({"role": entry["role"], "content": entry["content"]})
        messages.append({"role": "user", "content": user_msg})

        self.conversation_history.append({"role": "user", "content": user_msg})

        # Retry loop with exponential backoff
        last_error: Optional[Exception] = None
        for attempt in range(self.MAX_RETRIES):
            try:
                response: LLMResponse = self.llm.complete(
                    system=system,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
                assistant_msg = response.text
                self._consecutive_failures = 0

                logger.info(
                    "Agent %s LLM call OK: model=%s tokens=%d/%d latency=%.0fms",
                    self.name, response.model,
                    response.usage.get("input_tokens", 0),
                    response.usage.get("output_tokens", 0),
                    response.latency_ms,
                )
                self.conversation_history.append(
                    {"role": "assistant", "content": assistant_msg}
                )
                return assistant_msg

            except Exception as e:
                last_error = e
                self._consecutive_failures += 1
                delay = min(
                    self.RETRY_BASE_DELAY * (2 ** attempt),
                    self.RETRY_MAX_DELAY,
                )
                logger.warning(
                    "Agent %s LLM call failed (attempt %d/%d): %s. "
                    "Retrying in %.1fs...",
                    self.name, attempt + 1, self.MAX_RETRIES, e, delay,
                )
                if attempt < self.MAX_RETRIES - 1:
                    time.sleep(delay)

        # All retries exhausted — graceful degradation
        error_msg = (
            f"[Agent {self.name}] LLM unavailable after {self.MAX_RETRIES} attempts. "
            f"Last error: {last_error}. "
            f"Please retry later or check API key / network connectivity."
        )
        logger.error(error_msg)
        self.conversation_history.append(
            {"role": "assistant", "content": error_msg}
        )
        return error_msg

    def receive_and_process(self) -> list[Message]:
        """Read inbox, process each message, return response messages."""
        inbox = self.bus.get_inbox(self.role)
        responses = []
        for msg in inbox:
            context = (
                f"[Message from {msg.sender}] Subject: {msg.subject}\n\n{msg.payload}"
            )
            result = self.call_llm(context)

            response = Message(
                sender=self.role,
                recipient=msg.sender,
                msg_type=MessageType.RESPONSE,
                subject=f"Re: {msg.subject}",
                payload=result,
                in_reply_to=msg.id,
            )
            self.bus.post(response)
            responses.append(response)

            self.work_products.append({
                "request_id": msg.id,
                "subject": msg.subject,
                "output": result,
            })
        return responses

    def send_to(
        self,
        recipient: str,
        subject: str,
        payload: str,
        msg_type: MessageType = MessageType.REQUEST,
    ) -> str:
        msg = Message(
            sender=self.role, recipient=recipient,
            msg_type=msg_type, subject=subject, payload=payload,
        )
        return self.bus.post(msg)

    def broadcast(self, subject: str, payload: str) -> str:
        msg = Message(
            sender=self.role, recipient="all",
            msg_type=MessageType.BROADCAST, subject=subject, payload=payload,
        )
        return self.bus.post(msg)

    def handoff_to(self, recipient: str, subject: str, payload: str) -> str:
        msg = Message(
            sender=self.role, recipient=recipient,
            msg_type=MessageType.HANDOFF, subject=subject, payload=payload,
        )
        return self.bus.post(msg)

    def status(self) -> dict:
        return {
            "name": self.name,
            "role": self.role,
            "llm_provider": self.llm.provider_name,
            "messages_in_history": len(self.conversation_history),
            "work_products": len(self.work_products),
            "pending_inbox": len(self.bus.peek_inbox(self.role)),
            "consecutive_failures": self._consecutive_failures,
        }
