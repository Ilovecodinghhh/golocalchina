"""FastAPI application — GoLocalChina API."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import create_tables
from app.api.v1.auth import router as auth_router
from app.api.v1.guides import router as guides_router
from app.api.v1.service_requests import router as sr_router
from app.api.v1.profile import router as profile_router
from app.api.v1.listings import router as listings_router
from app.api.v1.explore import router as explore_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    # Auto-seed demo data if DB is empty (Railway wipes /tmp on redeploy)
    from seed_on_start import seed
    await seed()
    yield


app = FastAPI(
    title="GoLocalChina API",
    description="Information service platform connecting foreign tourists with local guides in China. Not a travel agency.",
    version="0.2.0",
    lifespan=lifespan,
)

origins = [o.strip() for o in settings.cors_origins.split(",")]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(auth_router, prefix="/api/v1")
app.include_router(guides_router, prefix="/api/v1")
app.include_router(sr_router, prefix="/api/v1")
app.include_router(profile_router, prefix="/api/v1")
app.include_router(listings_router, prefix="/api/v1")
app.include_router(explore_router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok", "platform": "GoLocalChina", "version": "0.2.0"}
