"""
LLM Provider Abstraction — Decouples agents from any specific LLM vendor.

Supports: Anthropic (Claude), OpenAI (GPT), and a Mock provider for testing.
Switch providers via LLM_PROVIDER env var or per-agent override.
"""
from __future__ import annotations

import os
import time
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Standardized response from any LLM provider."""
    text: str
    model: str
    provider: str
    usage: dict  # {"input_tokens": int, "output_tokens": int}
    latency_ms: float


class LLMProvider(ABC):
    """Abstract interface for LLM calls."""

    @abstractmethod
    def complete(
        self,
        system: str,
        messages: list[dict],
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> LLMResponse:
        """Send a chat completion request."""
        ...

    @abstractmethod
    def name(self) -> str:
        """Return provider name."""
        ...


class AnthropicProvider(LLMProvider):
    """Anthropic Claude via official Python SDK."""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        import anthropic
        key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise ValueError("ANTHROPIC_API_KEY not set")
        self._client = anthropic.Anthropic(api_key=key)
        self._model = model

    def name(self) -> str:
        return "anthropic"

    def complete(self, system, messages, max_tokens=4096, temperature=0.7) -> LLMResponse:
        t0 = time.monotonic()
        resp = self._client.messages.create(
            model=self._model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=messages,
        )
        latency = (time.monotonic() - t0) * 1000
        return LLMResponse(
            text=resp.content[0].text,
            model=self._model,
            provider="anthropic",
            usage={"input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens},
            latency_ms=latency,
        )


class OpenAIProvider(LLMProvider):
    """OpenAI GPT via official Python SDK."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        import openai
        key = api_key or os.environ.get("OPENAI_API_KEY")
        if not key:
            raise ValueError("OPENAI_API_KEY not set")
        self._client = openai.OpenAI(api_key=key)
        self._model = model

    def name(self) -> str:
        return "openai"

    def complete(self, system, messages, max_tokens=4096, temperature=0.7) -> LLMResponse:
        t0 = time.monotonic()
        full_messages = [{"role": "system", "content": system}] + messages
        resp = self._client.chat.completions.create(
            model=self._model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=full_messages,
        )
        latency = (time.monotonic() - t0) * 1000
        choice = resp.choices[0]
        return LLMResponse(
            text=choice.message.content or "",
            model=self._model,
            provider="openai",
            usage={
                "input_tokens": resp.usage.prompt_tokens if resp.usage else 0,
                "output_tokens": resp.usage.completion_tokens if resp.usage else 0,
            },
            latency_ms=latency,
        )


class MockProvider(LLMProvider):
    """Mock provider for testing — returns predictable responses."""

    def __init__(self, default_response: str = "[Mock LLM response]"):
        self._default = default_response

    def name(self) -> str:
        return "mock"

    def complete(self, system, messages, max_tokens=4096, temperature=0.7) -> LLMResponse:
        user_msg = messages[-1]["content"] if messages else ""
        return LLMResponse(
            text=f"{self._default}\nEcho: {user_msg[:100]}",
            model="mock-v1",
            provider="mock",
            usage={"input_tokens": len(system) + sum(len(m["content"]) for m in messages), "output_tokens": 50},
            latency_ms=5.0,
        )


# ---- Factory ----

_PROVIDERS = {
    "anthropic": AnthropicProvider,
    "openai": OpenAIProvider,
    "mock": MockProvider,
}


def get_provider(name: Optional[str] = None, **kwargs) -> LLMProvider:
    """Create an LLM provider by name. Defaults to LLM_PROVIDER env var or 'anthropic'."""
    provider_name = name or os.environ.get("LLM_PROVIDER", "anthropic").lower()
    if provider_name not in _PROVIDERS:
        raise ValueError(f"Unknown LLM provider: {provider_name}. Available: {list(_PROVIDERS.keys())}")
    return _PROVIDERS[provider_name](**kwargs)
