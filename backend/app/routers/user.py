# backend/app/routers/users.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db
from app.services import user_services
from app.schemas.user import  UserResponse

router = APIRouter(prefix="/users", tags=["Users"]) 

@router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    return await user_services.get_all_users(db)

@router.get("/names", response_model=list[str])
async def get_users_name(db: AsyncSession = Depends(get_db)):
    return await user_services.get_users_name(db)

