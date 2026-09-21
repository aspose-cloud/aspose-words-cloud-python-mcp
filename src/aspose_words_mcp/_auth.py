"""Outbound OAuth2 client-credentials auth to the real Aspose Cloud API (FR14).

This is a deliberate, self-contained copy of the builder's own `mcp_builder/auth/aspose_auth.py` —
never an import across the builder/published-package boundary (Sprint 7 requirements.md, Requirement
5.1, extended to every product package by Sprint 11).

Sprint 11 real bug fix: `v1.1` (and its matching `/oauth2/token` endpoint) is retired — confirmed
live, independently, that `v1.1` hangs on any upload above ~500 bytes, on two separate
machines/networks. The real, working API is `v4.0`, which requires a token from `/connect/token`
specifically (confirmed live: real uploads/downloads/document operations at realistic sizes). See
`mcp_builder/auth/aspose_auth.py`'s fuller writeup.
"""

from __future__ import annotations

import os
import time

import requests

TOKEN_URL = "https://api.aspose.cloud/connect/token"
_EXPIRY_SAFETY_BUFFER_SECONDS = 60.0

__all__ = ["AsposeAuthClient", "AsposeAuthError"]


class AsposeAuthError(Exception):
    """Wraps every network/transport failure from the Aspose Cloud OAuth2 token exchange."""


def _post_form(url: str, data: dict, *, timeout: float = 30.0) -> dict:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    try:
        response = requests.post(url, data=data, headers=headers, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise AsposeAuthError(f"Aspose Cloud token request to {url} failed: {exc}") from exc

    try:
        return response.json()
    except ValueError as exc:
        raise AsposeAuthError(f"Aspose Cloud token endpoint at {url} returned a non-JSON response: {exc}") from exc


class AsposeAuthClient:
    """Exchanges `ASPOSE_CLIENT_ID`/`ASPOSE_CLIENT_SECRET` for a cached, transparently-refreshed
    Aspose Cloud access token (FR14)."""

    def __init__(self, client_id: str | None = None, client_secret: str | None = None) -> None:
        self.client_id = client_id or os.environ.get("ASPOSE_CLIENT_ID")
        self.client_secret = client_secret or os.environ.get("ASPOSE_CLIENT_SECRET")

        if not self.client_id or not self.client_secret:
            raise ValueError(
                "AsposeAuthClient requires both a client_id and client_secret "
                "(pass explicitly or set ASPOSE_CLIENT_ID/ASPOSE_CLIENT_SECRET)."
            )

        self._token: str | None = None
        self._expires_at: float | None = None

    def _token_is_valid(self) -> bool:
        return (
            self._token is not None
            and self._expires_at is not None
            and time.monotonic() < self._expires_at
        )

    def _fetch_token(self) -> None:
        data = _post_form(
            TOKEN_URL,
            {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
        )

        try:
            token_type = data["token_type"]
            access_token = data["access_token"]
            expires_in = float(data["expires_in"])
        except (KeyError, TypeError, ValueError) as exc:
            raise AsposeAuthError(
                f"Aspose Cloud token endpoint returned an unexpected response shape: {data!r}"
            ) from exc

        self._token = f"{token_type} {access_token}"
        self._expires_at = time.monotonic() + max(expires_in - _EXPIRY_SAFETY_BUFFER_SECONDS, 0.0)

    def get_authorization_header(self) -> str:
        """Return a ready-to-use `Authorization` header value, refreshing first if needed.

        Raises:
            AsposeAuthError: on any network failure, non-2xx response, or malformed response body.
        """
        if not self._token_is_valid():
            self._fetch_token()
        assert self._token is not None
        return self._token
