"""Stubbed request interface for the load balancer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Optional, Protocol, runtime_checkable

from lb.Algorithm import Backend, Request


@dataclass(frozen=True)
class StubResponse:
    status_code: int
    body: bytes
    headers: Mapping[str, str]


@runtime_checkable
class RequestInterface(Protocol):
    def send_request(
        self,
        backend: Backend,
        request: Request,
    ) -> StubResponse:
        """Send a request without requiring a real server."""
        ...


class InMemoryRequestStub(RequestInterface):
    def __init__(self, response: Optional[StubResponse] = None) -> None:
        self._response = response or StubResponse(
            status_code=200,
            body=b"",
            headers={},
        )

    def send_request(
        self,
        backend: Backend,
        request: Request,
    ) -> StubResponse:
        return self._response
