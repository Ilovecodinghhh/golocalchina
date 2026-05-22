"""FastAPI application entrypoint.

Path B / compliance notes:
- "Service request" / "connection" / "listing" terminology only.
- No platform-held funds: all money movement goes through Airwallex
  destination charges; this app never touches a wallet/escrow.
- PIPL Art. 38: data-region pinned via Settings.data_region (default cn-hangzhou).
- OWASP: security headers, CORS allow-list, rate-limit hook, structured logs.
"""
from __future__ import annotations

import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging, log


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging(settings.debug)
    log.info(
        "app.startup",
        env=settings.env,
        data_region=settings.data_region,
        supported_locales=settings.supported_locales,
    )
    yield
    log.info("app.shutdown")


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Attach a request_id and locale to every request; emit timing log."""

    async def dispatch(self, request: Request, call_next):
        rid = request.headers.get("x-request-id") or str(uuid.uuid4())
        # i18n: honour Accept-Language but only allow supported locales
        al = request.headers.get("accept-language", settings.default_locale)
        locale = settings.default_locale
        for tag in (t.strip().split(";")[0] for t in al.split(",")):
            if tag in settings.supported_locales:
                locale = tag
                break
        request.state.request_id = rid
        request.state.locale = locale

        t0 = time.perf_counter()
        response = await call_next(request)
        dt_ms = (time.perf_counter() - t0) * 1000.0

        response.headers["x-request-id"] = rid
        response.headers["content-language"] = locale
        # OWASP baseline security headers
        response.headers["x-content-type-options"] = "nosniff"
        response.headers["x-frame-options"] = "DENY"
        response.headers["referrer-policy"] = "no-referrer"
        response.headers["strict-transport-security"] = "max-age=31536000; includeSubDomains"
        log.info(
            "http.request",
            request_id=rid,
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration_ms=round(dt_ms, 2),
            locale=locale,
        )
        return response


def create_app() -> FastAPI:
    app = FastAPI(
        title="GoLocalChina API",
        version="0.1.0",
        description=(
            "Two-sided intermediary platform connecting foreign visitors with "
            "licensed guides in China. Path B (information-intermediary) posture: "
            "no tour packages, no platform-held funds, guide-set pricing."
        ),
        openapi_url=f"{settings.api_v1_prefix}/openapi.json",
        docs_url=f"{settings.api_v1_prefix}/docs",
        redoc_url=f"{settings.api_v1_prefix}/redoc",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["x-request-id", "content-language"],
    )
    app.add_middleware(RequestContextMiddleware)

    @app.exception_handler(Exception)
    async def _unhandled(request: Request, exc: Exception):
        log.exception("http.unhandled", request_id=getattr(request.state, "request_id", None))
        return JSONResponse(
            status_code=500,
            content={"detail": "internal_server_error"},
        )

    app.include_router(api_router, prefix=settings.api_v1_prefix)
    return app


app = create_app()
