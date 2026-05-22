"""Structured logging with PII scrubbing (PIPL)."""
from __future__ import annotations

import logging
import re

import structlog

_PII_PATTERNS = [
    (re.compile(r'"password"\s*:\s*"[^"]*"'), '"password":"***"'),
    (re.compile(r'"email"\s*:\s*"[^"]*"'),    '"email":"***"'),
    (re.compile(r'"phone_e164"\s*:\s*"[^"]*"'), '"phone_e164":"***"'),
    (re.compile(r'"id_card_last4"\s*:\s*"[^"]*"'), '"id_card_last4":"***"'),
]


def _scrub_pii(_logger, _method, event_dict):
    for k, v in list(event_dict.items()):
        if isinstance(v, str):
            for pat, repl in _PII_PATTERNS:
                v = pat.sub(repl, v)
            event_dict[k] = v
    return event_dict


def configure_logging(debug: bool) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format="%(message)s")
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            _scrub_pii,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        cache_logger_on_first_use=True,
    )


log = structlog.get_logger()
