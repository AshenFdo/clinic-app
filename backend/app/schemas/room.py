from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RoomResponse(BaseModel):
    room_id: UUID
    room_num: str
    status: str

    model_config = ConfigDict(from_attributes=True)