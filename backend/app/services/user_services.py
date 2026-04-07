
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserUpdateRequest

#-----------------------------------
# Function to get all users
#  -----------------------------------

async def get_all_users(db:AsyncSession):
    try:
        result = await db.execute(select(User))
        users = result.scalars().all()

        if not users:
            return {"message": "No users found", "data": []}
        return users
    except Exception as e:
        print(f"Error fetching users: {e}")
        raise HTTPException(status_code=500, detail=str(e))

#-----------------------------------
# Function to get user by id (admin only)
#  -----------------------------------
async def get_user_by_id(user_id:str, db:AsyncSession)-> User:
    try:
        result = await db.execute(select(User).where(User.user_id == user_id))
        user = result.scalars().first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching user by id: {e}")
        raise HTTPException(status_code=500, detail=str(e))

#-----------------------------------
# Function to Update user profile
#  -----------------------------------

async def update_user(data: UserUpdateRequest, db: AsyncSession, current_user: User):
    try:
        result = await db.execute(select(User).where(User.user_id == current_user.user_id))
        user = result.scalars().first()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        update_data = data.model_dump(exclude_unset=True)
        # Keep password updates out of this profile update flow.
        update_data.pop("password", None)

        for field, value in update_data.items():
            if value is not None:
                setattr(user, field, value)

        await db.commit()
        await db.refresh(user)
        return user
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating user: {e}")
        raise HTTPException(status_code=500, detail=str(e))