
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date
from uuid import uuid4
from app.models.user import User

async def get_all_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User))
    return result.scalars().all()


async def get_users_name(db: AsyncSession) -> list[str]:
    result = await db.execute(select(User.full_name))
    return [row[0] for row in result.fetchall()]


async def create_mock_user(db: AsyncSession, full_name: str, gender: str) -> User:
    unique_suffix = uuid4().hex[:8]
    mock_user = User(
        full_name=full_name,
        Email=f"mock.user.{unique_suffix}@example.com",
        gender=gender,
        mobile_no="9999999999",
        profile_image_url="default-profile.png",
        date_of_birth=date(2000, 1, 1),
        password="mock_password",
        role="patient",
        is_active=1,
    )
    db.add(mock_user)
    await db.flush()
    await db.refresh(mock_user)
    return mock_user