"""Configuration loading for the Vehicle Service app.

Reads settings from environment variables (optionally from a local .env file)
and exposes a configured SDK client.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # python-dotenv is optional at runtime
    pass

from vehicle_service_collection_sdk import VehicleServiceCollectionSdk

DEFAULT_BASE_URL = "http://localhost:4501"


@dataclass
class Settings:
    """Runtime settings for the app."""

    base_url: str
    api_key: str | None
    timeout: float

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            base_url=os.getenv("VEHICLE_SERVICE_BASE_URL", DEFAULT_BASE_URL),
            api_key=os.getenv("VEHICLE_SERVICE_API_KEY") or None,
            timeout=float(os.getenv("VEHICLE_SERVICE_TIMEOUT", "30")),
        )


def build_client(settings: Settings | None = None) -> VehicleServiceCollectionSdk:
    """Create and configure the Vehicle Service SDK client."""
    settings = settings or Settings.from_env()
    return VehicleServiceCollectionSdk(
        api_key=settings.api_key,
        base_url=settings.base_url,
        timeout=settings.timeout,
    )
