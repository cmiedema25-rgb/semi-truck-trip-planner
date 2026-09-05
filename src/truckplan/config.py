"""Environment / settings for truckplan."""

from __future__ import annotations

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ors_api_key: Optional[str] = None
    truckplan_home_origin: str = "1200 Commerce Dr, Ontario, CA 91761"
    truckplan_force_mock: bool = False
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None

    @property
    def use_live_ors(self) -> bool:
        if self.truckplan_force_mock:
            return False
        return bool(self.ors_api_key and self.ors_api_key.strip())


@lru_cache
def get_settings() -> Settings:
    return Settings()
