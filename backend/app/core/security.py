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
    Verify a Supabase JWT access token using the JWKS endpoint.
        - Fetch the JWKS keys from Supabase
        - Use jose to decode and verify the token against the JWKS
        - Return the token payload if valid, or raise JWTError if invalid/expired.
    
    This function is used in the get_current_user dependency to authenticate API requests.
    """

    # Construct the JWKS URL based on the Supabase project URL
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
    
    # Decode and verify token using JWKS (jose automatically selects the correct key by kid)
    payload = jwt.decode(
        token,
        jwks,
        algorithms=["ES256"], # Supabase uses ES256 for access tokens
        audience="authenticated"  # Required by Supabase auth tokens
    )
    return payload






# -------------------------------------------------
#  functions for doctor invite tokens
# -------------------------------------------------
def generate_invite_token() -> str:
    """URL-safe 48-character token sent in doctor invite emails."""
    return secrets.token_urlsafe(36)
 
 
def invite_expiry(hours: int = 24) -> datetime:
    return datetime.now(timezone.utc) + timedelta(hours=hours)