"""Tiny translation registry for server-emitted user-facing messages.

We keep messages here (not in the DB) so they version-control with code.
Locales beyond the configured set fall back to en-US.
"""
from __future__ import annotations

from app.core.config import settings

_MESSAGES: dict[str, dict[str, str]] = {
    "en-US": {
        "service_request.created": "Your request has been sent to the guide.",
        "service_request.accepted": "The guide accepted your request.",
        "service_request.cancelled": "The request has been cancelled.",
        "auth.invalid_credentials": "Invalid email/phone or password.",
        "consent.required": "Consent is required before continuing.",
    },
    "zh-CN": {
        "service_request.created": "您的需求已发送给导游。",
        "service_request.accepted": "导游已接受您的需求。",
        "service_request.cancelled": "该需求已取消。",
        "auth.invalid_credentials": "邮箱/手机号或密码不正确。",
        "consent.required": "请先完成同意确认。",
    },
    "ja-JP": {
        "service_request.created": "リクエストをガイドに送信しました。",
        "service_request.accepted": "ガイドがリクエストを承諾しました。",
        "service_request.cancelled": "リクエストはキャンセルされました。",
        "auth.invalid_credentials": "メール／電話番号またはパスワードが正しくありません。",
        "consent.required": "続行する前に同意が必要です。",
    },
    "ko-KR": {
        "service_request.created": "요청이 가이드에게 전송되었습니다.",
        "service_request.accepted": "가이드가 요청을 수락했습니다.",
        "service_request.cancelled": "요청이 취소되었습니다.",
        "auth.invalid_credentials": "이메일/전화번호 또는 비밀번호가 잘못되었습니다.",
        "consent.required": "계속하려면 동의가 필요합니다.",
    },
    "fr-FR": {
        "service_request.created": "Votre demande a été envoyée au guide.",
        "service_request.accepted": "Le guide a accepté votre demande.",
        "service_request.cancelled": "La demande a été annulée.",
        "auth.invalid_credentials": "Identifiants invalides.",
        "consent.required": "Le consentement est requis avant de continuer.",
    },
}


def t(key: str, locale: str | None = None) -> str:
    loc = locale if locale in _MESSAGES else settings.default_locale
    table = _MESSAGES.get(loc, _MESSAGES[settings.default_locale])
    return table.get(key, key)
