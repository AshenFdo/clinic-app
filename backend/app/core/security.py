from jose import jwt, JWTError
from app.core.config import settings
from fastapi import HTTPException, status, Depends
import httpx

import secrets
from datetime import datetime, timedelta, timezone
 


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
    
    # Fetch the JWKS keys from Supabase 
    async with httpx.AsyncClient() as client:
        jwks = (await client.get(jwks_url)).json()
    
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