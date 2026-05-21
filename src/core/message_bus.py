"""
Message Bus — Inter-agent communication backbone.

All agents post messages to and read messages from this bus.
Each message has a sender, recipient(s), type, and payload.
"""
import time
import json
import uuid
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional
from collections import defaultdict


class MessageType(Enum):
    """Types of inter-agent messages."""
    REQUEST = "request"           # Ask another agent to do something
    RESPONSE = "response"         # Reply to a request
    BROADCAST = "broadcast"       # Announce to all agents
    HANDOFF = "handoff"           # Pass work product to next agent
    STATUS = "status"             # Status update
    ERROR = "error"               # Error report


class AgentRole(Enum):
    """The 4 active agent roles (no Analyst — deferred to post-launch)."""
    ARCHITECT = "architect"
    RESEARCHER = "researcher"
    LEGAL = "legal"
    BUILDER = "builder"
    ORCHESTRATOR = "orchestrator"  # The coordinator (you)


@dataclass
class Message:
    """A single message on the bus."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    sender: str = ""
    recipient: str = "all"         # agent role name or "all"
    msg_type: MessageType = MessageType.BROADCAST
    subject: str = ""
    payload: str = ""
    in_reply_to: Optional[str] = None
    timestamp: float = field(default_factory=time.time)

    def to_dict(self):
        d = asdict(self)
        d["msg_type"] = self.msg_type.value
        return d

    def summary(self):
        trunc = self.payload[:120] + "..." if len(self.payload) > 120 else self.payload
        return f"[{self.id}] {self.sender} → {self.recipient} ({self.msg_type.value}): {self.subject} | {trunc}"


class MessageBus:
    """
    Simple in-memory message bus with per-agent inboxes.
    Supports request/response, broadcast, and handoff patterns.
    """

    def __init__(self):
        self.messages: list[Message] = []
        self.inboxes: dict[str, list[Message]] = defaultdict(list)

    def post(self, msg: Message) -> str:
        """Post a message to the bus. Returns message ID."""
        self.messages.append(msg)
        if msg.recipient == "all":
            for role in AgentRole:
                if role.value != msg.sender:
                    self.inboxes[role.value].append(msg)
        else:
            self.inboxes[msg.recipient].append(msg)
        return msg.id

    def get_inbox(self, agent_role: str) -> list[Message]:
        """Get all unread messages for an agent."""
        msgs = self.inboxes[agent_role][:]
        self.inboxes[agent_role] = []
        return msgs

    def peek_inbox(self, agent_role: str) -> list[Message]:
        """Peek at inbox without consuming."""
        return self.inboxes[agent_role][:]

    def get_conversation(self, msg_id: str) -> list[Message]:
        """Get full conversation thread for a message."""
        thread = []
        for m in self.messages:
            if m.id == msg_id or m.in_reply_to == msg_id:
                thread.append(m)
        return sorted(thread, key=lambda x: x.timestamp)

    def get_full_log(self) -> list[dict]:
        """Get all messages as dicts."""
        return [m.to_dict() for m in self.messages]

    def summary(self) -> str:
        """Human-readable summary of all bus activity."""
        lines = [f"=== Message Bus: {len(self.messages)} messages ==="]
        for m in self.messages:
            lines.append(f"  {m.summary()}")
        pending = {k: len(v) for k, v in self.inboxes.items() if v}
        if pending:
            lines.append(f"  Pending inboxes: {pending}")
        return "\n".join(lines)
