from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine,async_sessionmaker
from sqlalchemy.engine import make_url
from app.core.config import settings


def _get_async_database_url(url: str) -> str:
    # Force async PostgreSQL driver to avoid fallback to psycopg2.
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


def _validate_database_url(url: str) -> None:
    parsed = make_url(url)
    # If host still contains '@', credentials were likely split incorrectly.
    if parsed.host and "@" in parsed.host:
        raise ValueError(
            "Invalid DATABASE_URL: host contains '@'. "
            "This usually means special characters in DB password are not URL-encoded "
            "(for example '@' should be '%40')."
        )


_validate_database_url(settings.DATABASE_URL)


engine = create_async_engine(
    _get_async_database_url(settings.DATABASE_URL),
    echo=settings.DEBUG,
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)