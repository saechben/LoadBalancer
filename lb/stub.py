"""Stubbed request interface for the load balancer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Optional, Protocol


@dataclass(frozen=True)
class StubResponse:
    status_code: int
    body: bytes
    headers: Mapping[str, str]

#simple interface
class RequestInterface(Protocol):
    def send_request(
        self,
        method: str,
        url: str,
        *,
        headers: Optional[Mapping[str, str]] = None,
        params: Optional[Mapping[str, str]] = None,
        body: Optional[bytes] = None,
        timeout: Optional[float] = None,
    ) -> StubResponse:
        """Send a request without requiring a real server."""

#stub for Request using the interface
class InMemoryRequestStub(RequestInterface):
    def __init__(self, response: Optional[StubResponse] = None) -> None:
        self._response = response or StubResponse(
            status_code=200,
            body=b"",
            headers={},
        )

    def send_request(
        self,
        method: str,
        url: str,
        *,
        headers: Optional[Mapping[str, str]] = None,
        params: Optional[Mapping[str, str]] = None,
        body: Optional[bytes] = None,
        timeout: Optional[float] = None,
    ) -> StubResponse:
        return self._response
