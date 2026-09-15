"""Fixed error taxonomy and internal rate-limit backoff (FR11, FR16).

**Deliberate, self-contained copy** of `mcp_builder/generated/_shared/errors.py` — this package must
have zero import dependency on `mcp_builder` (Sprint 7 requirements.md, Requirement 5.1).

Every tool in this package routes its real HTTP call through `call_with_taxonomy`, mapping the
response (or a transport failure) to one of exactly four `ToolErrorCode` values — never a per-tool ad
hoc shape, and never left to propagate as a raw exception. A `429` is retried with a bounded
exponential backoff before surfacing `rate_limited` — the calling agent never has to loop itself
(FR16); the retry cap is a fixed, small maximum (NFR9), never unbounded.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, Literal

import requests
from mcp.server.mcpserver.exceptions import ToolError as _MCPToolError

ToolErrorCode = Literal["bad_input", "auth_failure", "server_error", "rate_limited"]


@dataclass(frozen=True)
class ToolError(_MCPToolError):
    """Subclasses the MCP SDK's own `ToolError` (Sprint 11 real bug fix, found live via this exact
    package's first real error-path call) — see `mcp_builder/generated/_shared/errors.py`'s fuller
    writeup for why bare `Exception` silently discarded every real taxonomy code/message."""

    code: ToolErrorCode
    message: str

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"[{self.code}] {self.message}"


def _classify_response(response: requests.Response) -> ToolErrorCode | None:
    """Return the taxonomy code for a non-2xx response, or `None` if it's actually a success."""
    if response.ok:
        return None
    if response.status_code in (401, 403):
        return "auth_failure"
    if response.status_code == 429:
        return "rate_limited"
    if 400 <= response.status_code < 500:
        return "bad_input"
    return "server_error"


def call_with_taxonomy(
    fn: Callable[[], requests.Response],
    *,
    max_429_retries: int = 3,
    base_delay_seconds: float = 0.5,
    sleep: Callable[[float], None] = time.sleep,
) -> requests.Response:
    """Call `fn` (a zero-arg thunk performing one real HTTP request), mapping any failure into a
    `ToolError` with a fixed taxonomy code.

    A `429` response is retried up to `max_429_retries` times with exponential backoff
    (`base_delay_seconds * 2**attempt`) before raising `ToolError(code="rate_limited", ...)` — a fixed,
    capped retry (NFR9), never unbounded. Every other failure raises immediately, no retry.

    Raises:
        ToolError: on any non-2xx response or `requests.RequestException`.
    """
    attempt = 0
    while True:
        try:
            response = fn()
        except requests.RequestException as exc:
            raise ToolError(code="server_error", message=f"transport failure: {exc}") from exc

        code = _classify_response(response)
        if code is None:
            return response

        if code == "rate_limited" and attempt < max_429_retries:
            sleep(base_delay_seconds * (2**attempt))
            attempt += 1
            continue

        raise ToolError(code=code, message=f"HTTP {response.status_code}: {response.text[:500]}")
