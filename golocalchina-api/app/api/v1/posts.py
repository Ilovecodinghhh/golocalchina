"""Tourist Posts — tourists can create, view, and manage posts."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.post import TouristPost
from app.models.user import User

router = APIRouter(prefix="/posts", tags=["posts"])


class CreatePost(BaseModel):
    title: str = Field(min_length=5, max_length=200)
    content: str = Field(min_length=10)
    images: list[str] = []


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_post(
    author_user_id: str = Query(...),
    req: CreatePost = ...,
    db: AsyncSession = Depends(get_db),
):
    """Create a new tourist post."""
    post = TouristPost(
        author_user_id=author_user_id,
        title=req.title,
        content=req.content,
        images=req.images,
        is_done=False,
    )
    db.add(post)
    await db.flush()
    return {"id": post.id, "title": post.title, "message": "Post created"}


@router.get("")
async def list_posts(
    page: int = Query(1, ge=1),
    per_page: int = Query(30, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """List all posts with author info."""
    result = await db.execute(
        select(TouristPost).order_by(TouristPost.created_at.desc())
    )
    all_posts = result.scalars().all()

    posts_out = []
    for post in all_posts:
        user_result = await db.execute(
            select(User).where(User.id == post.author_user_id)
        )
        author = user_result.scalar_one_or_none()

        display_title = f"[DONE] {post.title}" if post.is_done else post.title

        posts_out.append({
            "id": post.id,
            "title": display_title,
            "content": post.content,
            "images": post.images if isinstance(post.images, list) else [],
            "is_done": post.is_done,
            "created_at": post.created_at,
            "author": {
                "user_id": author.id if author else "",
                "display_name": author.display_name if author else "Anonymous",
            }
        })

    total = len(posts_out)
    start = (page - 1) * per_page
    page_posts = posts_out[start:start + per_page]

    return {"posts": page_posts, "total": total, "page": page, "per_page": per_page}


@router.get("/{post_id}")
async def get_post(post_id: str, db: AsyncSession = Depends(get_db)):
    """Get a single post with author info."""
    result = await db.execute(
        select(TouristPost).where(TouristPost.id == post_id)
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    user_result = await db.execute(
        select(User).where(User.id == post.author_user_id)
    )
    author = user_result.scalar_one_or_none()

    display_title = f"[DONE] {post.title}" if post.is_done else post.title

    return {
        "id": post.id,
        "title": display_title,
        "content": post.content,
        "images": post.images if isinstance(post.images, list) else [],
        "is_done": post.is_done,
        "created_at": post.created_at,
        "author": {
            "user_id": author.id if author else "",
            "display_name": author.display_name if author else "Anonymous",
        }
    }


@router.put("/{post_id}/done")
async def mark_post_done(
    post_id: str,
    author_user_id: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """Mark a post as done. Only the author can do this."""
    result = await db.execute(
        select(TouristPost).where(
            TouristPost.id == post_id,
            TouristPost.author_user_id == author_user_id,
        )
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or not authorized")

    post.is_done = True
    await db.flush()
    return {"message": "Post marked as done"}


@router.delete("/{post_id}")
async def delete_post(
    post_id: str,
    author_user_id: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """Delete a post. Only the author can do this."""
    result = await db.execute(
        select(TouristPost).where(
            TouristPost.id == post_id,
            TouristPost.author_user_id == author_user_id,
        )
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or not authorized")

    await db.delete(post)
    await db.flush()
    return {"message": "Post deleted"}
