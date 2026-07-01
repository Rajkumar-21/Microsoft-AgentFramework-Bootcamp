"""Authentication & authorization.

Two modes (see ``REGISTRY_AUTH_MODE``):

* ``dev``   — local development. A static bearer token is accepted and mapped to
  a principal. Scopes can be simulated by sending
  ``Authorization: Bearer dev <space-separated-scopes>``. A bare ``Bearer dev``
  grants all scopes (admin) so the API is easy to explore locally.

* ``entra`` — Microsoft Entra ID. Bearer tokens are validated for signature
  (via the tenant JWKS), issuer, audience and expiry. Authorization is enforced
  from the ``scp`` (delegated) and ``roles`` (application) claims.

The same three logical permissions gate every write/govern path:
``Registry.Read`` < ``Registry.Publish`` < ``Registry.Manage``.
"""

from __future__ import annotations

from typing import Annotated

import jwt
from fastapi import Depends, Header, HTTPException, status
from jwt import PyJWKClient
from pydantic import BaseModel

from .config import Settings, get_settings

# Logical permissions used across the API.
SCOPE_READ = "Registry.Read"
SCOPE_PUBLISH = "Registry.Publish"
SCOPE_MANAGE = "Registry.Manage"
ALL_SCOPES = {SCOPE_READ, SCOPE_PUBLISH, SCOPE_MANAGE}


class Principal(BaseModel):
    """The verified caller — a user (delegated) or an app/agent (client creds)."""

    id: str
    name: str
    tenant_id: str = ""
    client_id: str = ""
    scopes: set[str] = set()
    is_app: bool = False

    def has(self, scope: str) -> bool:
        return scope in self.scopes


# --------------------------------------------------------------------------- #
# JWKS client (cached per process; handles key rollover internally)
# --------------------------------------------------------------------------- #
_jwk_client: PyJWKClient | None = None


def _jwks(settings: Settings) -> PyJWKClient:
    global _jwk_client
    if _jwk_client is None:
        _jwk_client = PyJWKClient(settings.entra_jwks_uri, cache_keys=True)
    return _jwk_client


def _principal_from_claims(claims: dict) -> Principal:
    # Delegated tokens carry `scp` (space-delimited); app tokens carry `roles`.
    scopes: set[str] = set()
    scp = claims.get("scp")
    if isinstance(scp, str):
        scopes |= {s for s in scp.split(" ") if s}
    roles = claims.get("roles")
    if isinstance(roles, list):
        scopes |= set(roles)

    is_app = "scp" not in claims  # client-credentials tokens have no scp
    # An agent app authorized to call the registry can at least read.
    if is_app and "Registry.Agent" in scopes:
        scopes.add(SCOPE_READ)

    name = (
        claims.get("name")
        or claims.get("preferred_username")
        or claims.get("azp")
        or claims.get("appid")
        or "unknown"
    )
    return Principal(
        id=claims.get("oid") or claims.get("sub") or "unknown",
        name=name,
        tenant_id=claims.get("tid", ""),
        client_id=claims.get("azp") or claims.get("appid", ""),
        scopes=scopes & ALL_SCOPES,
        is_app=is_app,
    )


def _validate_entra(token: str, settings: Settings) -> Principal:
    try:
        signing_key = _jwks(settings).get_signing_key_from_jwt(token).key
        claims = jwt.decode(
            token,
            signing_key,
            algorithms=["RS256"],
            audience=settings.entra_api_audience,
            issuer=settings.entra_issuer,
            options={"require": ["exp", "iss", "aud"]},
        )
    except jwt.PyJWTError as exc:  # signature/issuer/audience/expiry failures
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {exc}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    # Optionally restrict which client apps may call the API.
    allowed = settings.allowed_client_ids
    if allowed:
        azp = claims.get("azp") or claims.get("appid")
        if azp not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Client application is not authorized to call this API.",
            )
    return _principal_from_claims(claims)


def _principal_dev(token: str) -> Principal:
    # Format: "dev" or "dev Registry.Read Registry.Publish ..."
    parts = token.split()
    if not parts or parts[0] != "dev":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Dev mode expects 'Bearer dev [scopes...]'.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    requested = set(parts[1:]) & ALL_SCOPES
    scopes = requested or set(ALL_SCOPES)  # bare 'dev' == admin
    return Principal(
        id="dev-user",
        name="Local Developer",
        tenant_id="dev",
        client_id="dev",
        scopes=scopes,
        is_app=False,
    )


async def get_principal(
    authorization: Annotated[str | None, Header()] = None,
    settings: Annotated[Settings, Depends(get_settings)] = None,  # type: ignore[assignment]
) -> Principal:
    """FastAPI dependency: resolve and verify the caller from the bearer token."""
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = authorization[7:].strip()
    if settings.auth_mode == "entra":
        return _validate_entra(token, settings)
    return _principal_dev(token)


def require_scope(scope: str):
    """Build a dependency that requires ``scope`` (or the higher ``Manage``)."""

    async def _dep(
        principal: Annotated[Principal, Depends(get_principal)],
    ) -> Principal:
        if principal.has(scope) or principal.has(SCOPE_MANAGE):
            return principal
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"This operation requires the '{scope}' permission.",
        )

    return _dep


require_read = require_scope(SCOPE_READ)
require_publish = require_scope(SCOPE_PUBLISH)
require_manage = require_scope(SCOPE_MANAGE)
