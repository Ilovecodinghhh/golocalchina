"""Review schemas — tourist reviews and guide replies."""
from typing import Optional
from pydantic import BaseModel, Field


class CreateReview(BaseModel):
    """Tourist submits a review for a guide after service."""
    service_request_id: str
    stars: int = Field(ge=1, le=5, description="Rating from 1 to 5 stars")
    text: Optional[str] = Field(None, max_length=2000, description="Review text")


class GuideReply(BaseModel):
    """Guide replies to a tourist review."""
    reply_text: str = Field(..., min_length=1, max_length=1000, description="Guide's reply text")


class ReviewResponse(BaseModel):
    """Single review with optional guide reply."""
    id: str
    service_request_id: str
    reviewer_user_id: str
    reviewer_name: Optional[str] = None
    target_user_id: str
    stars: int
    text: Optional[str]
    guide_reply: Optional[str]
    guide_replied_at: Optional[str]
    created_at: str

    model_config = {"from_attributes": True}


class ReviewStats(BaseModel):
    """Aggregated rating statistics for a guide."""
    guide_user_id: str
    average_rating: float
    total_reviews: int
    distribution: dict  # {1: count, 2: count, 3: count, 4: count, 5: count}


class GuideReviewsResponse(BaseModel):
    """Paginated reviews for a guide with stats."""
    stats: ReviewStats
    reviews: list[ReviewResponse]
    total: int
    page: int
    page_size: int
