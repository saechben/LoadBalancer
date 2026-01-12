"""Load balancer core types and routing."""

from __future__ import annotations

from typing import Mapping, Optional, Sequence

from lb.Algorithm import Backend, Request, RoutingAlgorithm
from lb.stub import RequestInterface, StubResponse


class LoadBalancer:
    def __init__(
        self,
        backends: Sequence[Backend],
        algorithm: RoutingAlgorithm,
        requester: RequestInterface,
    ) -> None:
        self._algorithm = algorithm
        self._requester = requester
        self._algorithm.set_backends(backends)

    def set_backends(self, backends: Sequence[Backend]) -> None:
        self._algorithm.set_backends(backends)

    def handle_request(
        self,
        method: str,
        path: str,
        *,
        headers: Optional[Mapping[str, str]] = None,
        params: Optional[Mapping[str, str]] = None,
        body: Optional[bytes] = None,
        timeout: Optional[float] = None,
        client_id: Optional[str] = None,
    ) -> StubResponse:
        request = Request(
            method=method,
            path=path,
            headers=headers or {},
            params=params or {},
            body=body,
            timeout=timeout,
            client_id=client_id,
        )
        backend = self._algorithm.select(request)
        return self._requester.send_request(backend, request)
