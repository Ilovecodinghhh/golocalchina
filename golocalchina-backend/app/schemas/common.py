"""Shared Pydantic schemas."""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PaginatedResponse(ORMBase, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int


class IDResponse(BaseModel):
    id: uuid.UUID


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str
    version: str
    server_time: datetime = Field(default_factory=datetime.utcnow)
