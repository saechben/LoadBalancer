"""Routing algorithm types and implementations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Optional, Protocol, Sequence


@dataclass(frozen=True)
class Backend:
    name: str
    base_url: str


@dataclass(frozen=True)
class Request:
    method: str
    path: str
    headers: Mapping[str, str] = field(default_factory=dict)
    params: Mapping[str, str] = field(default_factory=dict)
    body: Optional[bytes] = None
    timeout: Optional[float] = None
    client_id: Optional[str] = None


class RoutingAlgorithm(Protocol):
    def set_backends(self, backends: Sequence[Backend]) -> None:
        """Provide the destinations this algorithm can route to."""
        ...

    def select(self, request: Request) -> Backend:
        """Choose a backend for a single request."""
        ...


class RoundRobinAlgorithm(RoutingAlgorithm):
    def __init__(self) -> None:
        self._backends: list[Backend] = []
        self._index = 0

    def set_backends(self, backends: Sequence[Backend]) -> None:
        self._backends = list(backends)
        self._index = 0

    def select(self, request: Request) -> Backend:
        if not self._backends:
            raise ValueError("No backends configured")
        backend = self._backends[self._index]
        self._index = (self._index + 1) % len(self._backends)
        return backend


class StickyRoundRobinAlgorithm(RoutingAlgorithm):
    def __init__(self) -> None:
        self._backends: list[Backend] = []
        self._index = 0
        self._affinity: dict[str, Backend] = {}

    def set_backends(self, backends: Sequence[Backend]) -> None:
        self._backends = list(backends)
        self._index = 0
        if not self._backends:
            self._affinity.clear()
            return
        allowed = set(self._backends)
        self._affinity = {
            key: backend
            for key, backend in self._affinity.items()
            if backend in allowed
        }

    def select(self, request: Request) -> Backend:
        if not self._backends:
            raise ValueError("No backends configured")
        key = request.client_id
        if key:
            backend = self._affinity.get(key)
            if backend is not None:
                return backend
        backend = self._backends[self._index]
        self._index = (self._index + 1) % len(self._backends)
        if key:
            self._affinity[key] = backend
        return backend
