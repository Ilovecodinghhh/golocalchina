"""
Message Bus — Inter-agent communication backbone with SQLite persistence.

Messages survive process restarts. Each message has sender, recipient(s),
type, payload, and timestamps. Supports request/response, broadcast,
and handoff patterns.
"""
from __future__ import annotations

import json
import os
import sqlite3
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional
from collections import defaultdict


class MessageType(Enum):
    REQUEST = "request"
    RESPONSE = "response"
    BROADCAST = "broadcast"
    HANDOFF = "handoff"
    STATUS = "status"
    ERROR = "error"


class AgentRole(Enum):
    ARCHITECT = "architect"
    RESEARCHER = "researcher"
    LEGAL = "legal"
    BUILDER = "builder"
    ORCHESTRATOR = "orchestrator"


@dataclass
class Message:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    sender: str = ""
    recipient: str = "all"
    msg_type: MessageType = MessageType.BROADCAST
    subject: str = ""
    payload: str = ""
    in_reply_to: Optional[str] = None
    timestamp: float = field(default_factory=time.time)
    read: bool = False

    def to_dict(self) -> dict:
        d = asdict(self)
        d["msg_type"] = self.msg_type.value
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Message":
        d = dict(d)
        d["msg_type"] = MessageType(d["msg_type"])
        return cls(**d)

    def summary(self) -> str:
        trunc = self.payload[:120] + "..." if len(self.payload) > 120 else self.payload
        return f"[{self.id}] {self.sender} -> {self.recipient} ({self.msg_type.value}): {self.subject} | {trunc}"


_SCHEMA = """
CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    sender TEXT NOT NULL,
    recipient TEXT NOT NULL DEFAULT 'all',
    msg_type TEXT NOT NULL,
    subject TEXT NOT NULL DEFAULT '',
    payload TEXT NOT NULL DEFAULT '',
    in_reply_to TEXT,
    timestamp REAL NOT NULL,
    read INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_recipient_read ON messages(recipient, read);
CREATE INDEX IF NOT EXISTS idx_timestamp ON messages(timestamp);
"""


class MessageBus:
    """
    SQLite-backed message bus with per-agent inboxes.
    Messages persist across restarts. Backward-compatible with
    the original in-memory API.
    """

    def __init__(self, db_path: Optional[str] = None):
        self._db_path = db_path or os.environ.get("MESSAGE_BUS_DB", ":memory:")
        self._conn = sqlite3.connect(self._db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    @contextmanager
    def _cursor(self):
        cur = self._conn.cursor()
        try:
            yield cur
            self._conn.commit()
        except Exception:
            self._conn.rollback()
            raise
        finally:
            cur.close()

    def post(self, msg: Message) -> str:
        """Post a message. Returns message ID."""
        with self._cursor() as cur:
            cur.execute(
                """INSERT INTO messages (id, sender, recipient, msg_type, subject, payload, in_reply_to, timestamp, read)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)""",
                (msg.id, msg.sender, msg.recipient, msg.msg_type.value,
                 msg.subject, msg.payload, msg.in_reply_to, msg.timestamp),
            )
        return msg.id

    def get_inbox(self, agent_role: str) -> list[Message]:
        """Get all unread messages for an agent, mark them as read."""
        with self._cursor() as cur:
            # For broadcast messages (recipient='all'), deliver to everyone except sender
            cur.execute(
                """SELECT * FROM messages
                   WHERE (recipient = ? OR recipient = 'all')
                     AND read = 0 AND sender != ?
                   ORDER BY timestamp""",
                (agent_role, agent_role),
            )
            rows = cur.fetchall()
            ids = [r["id"] for r in rows]
            if ids:
                placeholders = ",".join("?" * len(ids))
                cur.execute(f"UPDATE messages SET read = 1 WHERE id IN ({placeholders})", ids)
        return [self._row_to_message(r) for r in rows]

    def peek_inbox(self, agent_role: str) -> list[Message]:
        """Peek at inbox without consuming."""
        with self._cursor() as cur:
            cur.execute(
                """SELECT * FROM messages
                   WHERE (recipient = ? OR recipient = 'all')
                     AND read = 0 AND sender != ?
                   ORDER BY timestamp""",
                (agent_role, agent_role),
            )
            return [self._row_to_message(r) for r in cur.fetchall()]

    def get_conversation(self, msg_id: str) -> list[Message]:
        """Get full conversation thread for a message."""
        with self._cursor() as cur:
            cur.execute(
                "SELECT * FROM messages WHERE id = ? OR in_reply_to = ? ORDER BY timestamp",
                (msg_id, msg_id),
            )
            return [self._row_to_message(r) for r in cur.fetchall()]

    def get_full_log(self) -> list[dict]:
        """Get all messages as dicts."""
        with self._cursor() as cur:
            cur.execute("SELECT * FROM messages ORDER BY timestamp")
            return [self._row_to_message(r).to_dict() for r in cur.fetchall()]

    def message_count(self) -> int:
        with self._cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM messages")
            return cur.fetchone()[0]

    def summary(self) -> str:
        total = self.message_count()
        lines = [f"=== Message Bus: {total} messages (db: {self._db_path}) ==="]
        with self._cursor() as cur:
            cur.execute("SELECT * FROM messages ORDER BY timestamp LIMIT 50")
            for r in cur.fetchall():
                lines.append(f"  {self._row_to_message(r).summary()}")
        return "\n".join(lines)

    def close(self):
        self._conn.close()

    @staticmethod
    def _row_to_message(row: sqlite3.Row) -> Message:
        return Message(
            id=row["id"],
            sender=row["sender"],
            recipient=row["recipient"],
            msg_type=MessageType(row["msg_type"]),
            subject=row["subject"],
            payload=row["payload"],
            in_reply_to=row["in_reply_to"],
            timestamp=row["timestamp"],
            read=bool(row["read"]),
        )
