from datetime import datetime

from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import DateTime, func, Datefrom, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase): ...

class User(Base):
    __tablename__ = "t_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False)

    password: Mapped[str] = mapped_column(nullable=False)

    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    last_update: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    tear: Mapped[int] = mapped_column(nullable=False)

class Ad(Base):
    __table__ = "t_ads"

    id: Mapped[int] = mapped_column(primary_key=True)

    brand: Mapped[str]
    
    horsepower: Mapped[float]
    volume: Mapped[float]
