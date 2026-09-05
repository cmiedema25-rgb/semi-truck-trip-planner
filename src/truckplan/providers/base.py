"""Abstract provider interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from truckplan.models import GeoPoint, RouteResult, VehicleProfile


class Provider(ABC):
    name: str = "base"

    @abstractmethod
    def geocode(self, address: str) -> GeoPoint:
        """Resolve a free-text address to coordinates."""

    @abstractmethod
    def route(
        self,
        origin: GeoPoint,
        destination: GeoPoint,
        vehicle: VehicleProfile,
    ) -> RouteResult:
        """Compute an HGV-oriented route between two points."""
