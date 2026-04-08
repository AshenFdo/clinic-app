from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db , require_role
from app.services.room_services import get_all_rooms
from app.schemas.room import RoomResponse


router = APIRouter(prefix="/room", tags=["Room"])

# -----------------------------------
# API router to get all rooms 
# -----------------------------------
@router.get("/all", response_model=list[RoomResponse], dependencies=[Depends(require_role("admin"))])
async def read_all_rooms(
    db: AsyncSession = Depends(get_db),
):
    return await get_all_rooms(db)