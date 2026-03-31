from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import Column, DateTime, func

class Base(DeclarativeBase):
    '''Base class for all models in the application.'''

    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
