"""Application configuration, loaded from environment / .env file."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Strongly-typed settings for the registry service."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Auth ---
    auth_mode: Literal["dev", "entra"] = Field("dev", alias="REGISTRY_AUTH_MODE")
    entra_tenant_id: str = Field("", alias="ENTRA_TENANT_ID")
    entra_api_audience: str = Field("", alias="ENTRA_API_AUDIENCE")
    entra_allowed_client_ids: str = Field("", alias="ENTRA_ALLOWED_CLIENT_IDS")

    # --- Storage ---
    store: Literal["memory", "cosmos"] = Field("memory", alias="REGISTRY_STORE")
    cosmos_endpoint: str = Field("", alias="COSMOS_ENDPOINT")
    cosmos_database: str = Field("agentregistry", alias="COSMOS_DATABASE")
    cosmos_key: str = Field("", alias="COSMOS_KEY")

    # --- App ---
    seed: bool = Field(True, alias="REGISTRY_SEED")
    cors_origins: str = Field("http://localhost:5173", alias="CORS_ORIGINS")

    @property
    def allowed_client_ids(self) -> list[str]:
        return [c.strip() for c in self.entra_allowed_client_ids.split(",") if c.strip()]

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def entra_issuer(self) -> str:
        # v2.0 issuer for a single-tenant app registration.
        return f"https://login.microsoftonline.com/{self.entra_tenant_id}/v2.0"

    @property
    def entra_jwks_uri(self) -> str:
        return (
            f"https://login.microsoftonline.com/{self.entra_tenant_id}"
            "/discovery/v2.0/keys"
        )


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()
