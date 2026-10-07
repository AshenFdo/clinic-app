from jose import jwt, JWTError
from app.core.config import settings
from fastapi import HTTPException, status
import httpx

import secrets
from datetime import datetime, timedelta, timezone


_JWKS_CACHE: dict | None = None
_JWKS_CACHE_AT: datetime | None = None
_JWKS_CACHE_TTL_SECONDS = 300
 


# -------------------------------------------------
#  JWT verification Function
# -------------------------------------------------

async def verify_supabase_token(token: str) -> dict:
    """
    Verify a Supabase JWT access token using its configured signing method.
        - Verify HS256 tokens with the configured JWT secret
        - Fetch JWKS keys from Supabase for ES256 tokens
        - Use jose to decode and verify the token
        - Return the token payload if valid, or raise JWTError if invalid/expired.
    
    This function is used in the get_current_user dependency to authenticate API requests.
    """

    try:
        algorithm = jwt.get_unverified_header(token).get("alg")
    except JWTError:
        raise JWTError("Invalid token header")

    if algorithm == "HS256":
        key = settings.SUPABASE_JWT_SECRET
    elif algorithm == "ES256":
        key = await _get_supabase_jwks()
    else:
        raise JWTError("Unsupported token algorithm")

    return jwt.decode(
        token,
        key,
        algorithms=[algorithm],
        audience="authenticated",
    )


async def _get_supabase_jwks() -> dict:
    """Fetch and cache the public keys used by ES256 Supabase tokens."""
    jwks_url = f"{settings.SUPABASE_URL}/auth/v1/.well-known/jwks.json"

    # Reuse recently fetched keys to avoid a network call on every request.
    global _JWKS_CACHE, _JWKS_CACHE_AT
    now = datetime.now(timezone.utc)
    if (
        _JWKS_CACHE is not None
        and _JWKS_CACHE_AT is not None
        and (now - _JWKS_CACHE_AT).total_seconds() < _JWKS_CACHE_TTL_SECONDS
    ):
        jwks = _JWKS_CACHE
    else:
        try:
            timeout = httpx.Timeout(connect=10.0, read=10.0, write=10.0, pool=10.0)
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(jwks_url)
                response.raise_for_status()
                jwks = response.json()
            _JWKS_CACHE = jwks
            _JWKS_CACHE_AT = now
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication provider timeout",
            )
        except httpx.HTTPError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication provider unavailable",
            )
    
    return jwks






# -------------------------------------------------
#  functions for doctor invite tokens
# -------------------------------------------------
def generate_invite_token() -> str:
    """URL-safe 48-character token sent in doctor invite emails."""
    return secrets.token_urlsafe(36)
 
 
def invite_expiry(hours: int = 24) -> datetime:
    return datetime.now(timezone.utc) + timedelta(hours=hours)