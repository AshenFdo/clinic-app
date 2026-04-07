# backend/app/routers/users.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db , get_current_user
from app.services.user_services import get_all_users, get_user_by_id, update_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdateRequest

router = APIRouter(prefix="/users", tags=["Users"]) 

# -----------------------------------
# API endpoint to get Current User Profile
# -----------------------------------
@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: UserResponse = Depends(get_current_user)):
    """Get the currently authenticated user's profile."""
    return current_user


# -----------------------------------
# API endpoint to get all users (admin only)
# -----------------------------------
@router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    """Get a list of all users. Admin access required."""
    return await get_all_users(db)

# -----------------------------------
# API endpoint to get user by id (admin only)
# -----------------------------------
@router.get("/{userId}", response_model=UserResponse)
async def read_user_by_id(user_id:str, db: AsyncSession = Depends(get_db)) -> User:
    """Get a user by their ID. Admin access required."""
    return await get_user_by_id(user_id, db)


# -----------------------------------
# API endpoint to update current user profile
# -----------------------------------
@router.patch("/me", response_model=UserResponse)
async def update_my_profile(
    data: UserUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> User:
    """Update the current user's profile. Admin access required."""
    return await update_user(data, db, current_user)
