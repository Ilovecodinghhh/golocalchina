"""FastAPI application — GoLocalChina API (Path B: Information Service Platform)."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import create_tables
from app.api.v1.auth import router as auth_router
from app.api.v1.guides import router as guides_router
from app.api.v1.service_requests import router as service_requests_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(
    title="GoLocalChina API",
    description=(
        "Information service platform connecting foreign tourists with "
        "independently licensed tour guides in China. "
        "This platform is NOT a travel agency (非旅行社). We do not process payments."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

origins = [o.strip() for o in settings.cors_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(guides_router, prefix="/api/v1")
app.include_router(service_requests_router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok", "platform": "GoLocalChina", "role": "information_service_platform"}
