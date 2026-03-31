from typing import AsyncGenerator
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from jose import JWTError
from app.core.security import verify_supabase_token
from app.models.user import User


# Define the HTTP Bearer scheme for token authentication
bearer_scheme  = HTTPBearer()


# ---------------------------------------------------
# Dependency to get DB session for each request
# ---------------------------------------------------
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide one AsyncSession per request.

    The session is yielded to route/service code, then:
    - commit runs if request handling finishes without error
    - rollback runs if an exception is raised
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# ---------------------------------------------------
# Dependency to get current authenticated user from Bearer token
# ---------------------------------------------------
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Resolve the authenticated user from a Bearer token.

    Flow:
    1) Read token from Authorization header
    2) Verify token against Supabase JWKS
    3) Load matching user row from local database
    4) Return User object or raise 401/404 HTTPException on failure
    """
    token = credentials.credentials

    try:
        # Verify token and extract payload (this will raise JWTError if invalid)
        payload = await verify_supabase_token(token)
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate token")

    # Load user from database using user_id from token payload
    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found in DB")
    return user


# ---------------------------------------------------
# Role-based access control dependency
# ---------------------------------------------------
def require_role(*roles: str):
    """
    Enforce allowed roles on a route.

    Usage:
    Depends(require_role("Admin", "Doctor","Patient"))
    """

    # Normalize roles to lowercase and strip whitespaces 
    normalized_roles = {
        role.lower().strip()
        for role in roles
        if role and role.strip()
    }

    if not normalized_roles:
        raise ValueError("require_role needs at least one non-empty role")

    # Function that used as dependency to check the user's role against allowed roles
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        user_role = current_user.role.lower().strip() if current_user.role else ""

        if user_role not in normalized_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return role_checker