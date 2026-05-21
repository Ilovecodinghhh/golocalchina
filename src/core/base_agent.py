"""
Base Agent — Abstract agent class all sub-agents inherit from.

Uses Claude Code CLI (`claude --print`) as the LLM backend.
Each agent has a system prompt, skills context, and access to the message bus.
"""
import os
import subprocess
import json
import tempfile
from abc import ABC, abstractmethod
from src.core.message_bus import MessageBus, Message, MessageType


class BaseAgent(ABC):
    """Base class for all sub-agents."""

    def __init__(self, name: str, role: str, bus: MessageBus):
        self.name = name
        self.role = role
        self.bus = bus
        self.conversation_history: list[dict] = []
        self.work_products: list[dict] = []

    @abstractmethod
    def system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        pass

    @abstractmethod
    def skills_context(self) -> str:
        """Return loaded skills/knowledge context for this agent."""
        pass

    def call_llm(self, user_msg: str, max_tokens: int = 4096) -> str:
        """Make an LLM call via Claude Code CLI."""
        full_system = self.system_prompt() + "\n\n" + self.skills_context()[:8000]

        # Build the prompt including conversation history context
        history_context = ""
        if self.conversation_history:
            history_context = "\n\n--- PREVIOUS CONVERSATION ---\n"
            for entry in self.conversation_history[-4:]:  # Last 2 exchanges
                role_label = "You said" if entry["role"] == "assistant" else "User said"
                history_context += f"\n{role_label}:\n{entry['content'][:500]}\n"
            history_context += "\n--- END PREVIOUS CONVERSATION ---\n"

        full_prompt = f"""SYSTEM INSTRUCTIONS:
{full_system}
{history_context}
CURRENT REQUEST:
{user_msg}"""

        self.conversation_history.append({"role": "user", "content": user_msg})

        try:
            # Pipe the prompt via stdin to avoid shell arg length limits
            result = subprocess.run(
                ["claude", "--print", "--dangerously-skip-permissions"],
                input=full_prompt,
                capture_output=True,
                text=True,
                timeout=300,
            )
            assistant_msg = result.stdout.strip()
            if not assistant_msg:
                assistant_msg = f"[Agent {self.name} produced no output. stderr: {result.stderr[:200]}]"
        except subprocess.TimeoutExpired:
            assistant_msg = f"[Agent {self.name} timed out after 300s]"
        except Exception as e:
            assistant_msg = f"[Agent {self.name} error: {e}]"

        self.conversation_history.append({"role": "assistant", "content": assistant_msg})
        return assistant_msg

    def receive_and_process(self) -> list[Message]:
        """Read inbox, process each message, return response messages."""
        inbox = self.bus.get_inbox(self.role)
        responses = []
        for msg in inbox:
            context = f"[Message from {msg.sender}] Subject: {msg.subject}\n\n{msg.payload}"
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

    def send_to(self, recipient: str, subject: str, payload: str,
                msg_type: MessageType = MessageType.REQUEST) -> str:
        """Send a message to another agent."""
        msg = Message(
            sender=self.role,
            recipient=recipient,
            msg_type=msg_type,
            subject=subject,
            payload=payload,
        )
        return self.bus.post(msg)

    def broadcast(self, subject: str, payload: str) -> str:
        """Broadcast to all agents."""
        msg = Message(
            sender=self.role,
            recipient="all",
            msg_type=MessageType.BROADCAST,
            subject=subject,
            payload=payload,
        )
        return self.bus.post(msg)

    def handoff_to(self, recipient: str, subject: str, payload: str) -> str:
        """Hand off a work product to the next agent in the pipeline."""
        msg = Message(
            sender=self.role,
            recipient=recipient,
            msg_type=MessageType.HANDOFF,
            subject=subject,
            payload=payload,
        )
        return self.bus.post(msg)

    def status(self) -> dict:
        return {
            "name": self.name,
            "role": self.role,
            "messages_in_history": len(self.conversation_history),
            "work_products": len(self.work_products),
            "pending_inbox": len(self.bus.peek_inbox(self.role)),
        }
