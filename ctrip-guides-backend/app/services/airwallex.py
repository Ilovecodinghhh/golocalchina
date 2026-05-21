"""Airwallex PSP client — destination-charges pattern.

Path B / payments compliance posture:
- The GUIDE is the merchant-of-record on the PSP side (a separate connected
  account on Airwallex), so funds settle PSP → guide DIRECTLY.
- This platform NEVER holds funds. No wallet/escrow table exists.
- The platform's intermediary commission is split off by the PSP into a
  *separate* service-fee invoice on the platform's own account — it is not
  taken out of a held balance.
- All network calls go via httpx async; auth is OAuth2 client-credentials.
- This module is the ONLY place that talks to the PSP. All callers go
  through `AirwallexClient.create_payment_intent_for_request`, which
  enforces destination = guide.psp_account_id.

Reference: Airwallex Connected Accounts / Payment Intents API.
"""
from __future__ import annotations

import time
import uuid
from decimal import Decimal
from typing import Any, Optional

import httpx

from app.core.config import settings
from app.core.logging import log


class AirwallexError(RuntimeError):
    pass


class AirwallexClient:
    """Thin async wrapper around Airwallex REST.

    NB: In dev/test, when no credentials are configured we operate in
    `simulate=True` mode and return deterministic stub payloads so the
    rest of the system can be exercised end-to-end. The simulator still
    enforces the destination-charge invariant (guide MoR).
    """

    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        client_id: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        self.base_url = base_url or settings.airwallex_api_base
        self.client_id = client_id or settings.airwallex_client_id
        self.api_key = api_key or settings.airwallex_api_key
        self.simulate = not (self.client_id and self.api_key)
        self._token: Optional[str] = None
        self._token_exp: float = 0.0

    async def _auth_header(self) -> dict[str, str]:
        if self.simulate:
            return {"x-simulate": "1"}
        now = time.time()
        if not self._token or now > self._token_exp - 60:
            async with httpx.AsyncClient(timeout=10) as cli:
                r = await cli.post(
                    f"{self.base_url}/api/v1/authentication/login",
                    headers={
                        "x-client-id": self.client_id,
                        "x-api-key": self.api_key,
                    },
                )
                r.raise_for_status()
                data = r.json()
                self._token = data["token"]
                # token TTL ~30min per Airwallex docs
                self._token_exp = now + 25 * 60
        return {"Authorization": f"Bearer {self._token}"}

    async def create_payment_intent_for_request(
        self,
        *,
        request_id: uuid.UUID,
        amount: Decimal,
        currency: str,
        guide_psp_account: str,
        platform_commission: Decimal,
        idempotency_key: Optional[str] = None,
    ) -> dict[str, Any]:
        """Create a destination-charge payment intent.

        INVARIANT: `guide_psp_account` MUST be set — otherwise we'd implicitly
        capture funds into the platform's account, which violates Path B and
        the《非金融机构支付服务管理办法》 licensure boundary.
        """
        if not guide_psp_account:
            raise AirwallexError(
                "destination_account_required: refusing to create an intent "
                "without a guide connected-account (would imply platform custody)"
            )

        idem = idempotency_key or str(uuid.uuid4())
        payload = {
            "request_id": str(request_id),
            "amount": str(amount),
            "currency": currency,
            "merchant_order_id": str(request_id),
            # destination = guide; commission is a fee taken by the platform
            "transfer_data": {"destination": guide_psp_account},
            "application_fee_amount": str(platform_commission),
            "metadata": {
                "service_request_id": str(request_id),
                # explicit marker that platform is intermediary, not principal
                "platform_role": "intermediary",
            },
        }

        if self.simulate:
            stub_id = f"int_sim_{uuid.uuid4().hex[:24]}"
            log.info(
                "airwallex.simulated_intent",
                request_id=str(request_id),
                amount=str(amount),
                currency=currency,
                destination=guide_psp_account,
                commission=str(platform_commission),
            )
            return {
                "id": stub_id,
                "client_secret": f"cs_sim_{uuid.uuid4().hex}",
                "amount": str(amount),
                "currency": currency,
                "status": "REQUIRES_PAYMENT_METHOD",
                "transfer_data": payload["transfer_data"],
                "application_fee_amount": payload["application_fee_amount"],
            }

        headers = await self._auth_header()
        headers["x-idempotency-key"] = idem
        async with httpx.AsyncClient(timeout=10) as cli:
            r = await cli.post(
                f"{self.base_url}/api/v1/pa/payment_intents/create",
                headers=headers,
                json=payload,
            )
            if r.status_code >= 400:
                raise AirwallexError(f"psp_error:{r.status_code}:{r.text[:200]}")
            return r.json()


def get_airwallex() -> AirwallexClient:
    return AirwallexClient()
