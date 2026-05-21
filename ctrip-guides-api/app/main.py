"""FastAPI application — Ctrip-Guides API (Path B: Information Service Platform)."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.auth import router as auth_router
from app.api.v1.guides import router as guides_router
from app.api.v1.service_requests import router as service_requests_router

app = FastAPI(
    title="Ctrip-Guides API",
    description=(
        "Information service platform connecting foreign tourists with "
        "independently licensed tour guides in China. "
        "This platform is NOT a travel agency (非旅行社)."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API v1 routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(guides_router, prefix="/api/v1")
app.include_router(service_requests_router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok", "platform": "Ctrip-Guides", "role": "information_service_platform"}
