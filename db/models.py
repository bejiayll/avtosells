from datetime import datetime

from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import DateTime, func, Datefrom, ForeignKey, String, CheckConstraint
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

    ads: Mapped[list["Ad"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    reviews: Mapped[list["Review"]]

    tear: Mapped[int] = mapped_column(nullable=False)

    reviews_sent: Mapped[list["Review"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    reviews_received: Mapped[list["Review"]] = relationship(back_populates="target", cascade="all, delete-orphan")

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="topicstarter")
    messages: Mapped[list["Message"]] = relationship(back_populates="author")


class Ad(Base):
    __table__ = "t_ads"

    id: Mapped[int] = mapped_column(primary_key=True)

    brand: Mapped[str] = mapped_column(nullable=False)
    
    horsepower: Mapped[float] = mapped_column(nullable=False)
    volume: Mapped[float] = mapped_column(nullable=False)

    gearbox_steps: Mapped[int] = mapped_column(nullable=False)
    gearbox: Mapped[int] = mapped_column(nullable=False) # 1: manual | 2: robot | 3: automatic

    production_year: Mapped[int] = mapped_column(nullable=False)

    images: Mapped[list[str]] = mapped_column(ARRAY(String))

    author: Mapped[int] = relationship(back_populates="ads")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    __table_args__ = (
        CheckConstraint('production_year >= 1945', name='year_limit')
    )


class Review(Base):
    __tablename__ = "t_reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    author_id: Mapped[int] = mapped_column(ForeignKey("t_users.id"), nullable=False)
    target_id: Mapped[int] = mapped_column(ForeignKey("t_users.id"), nullable=False)

    author: Mapped["User"] = relationship(back_populates="reviews_sent")
    target: Mapped["User"] = relationship(back_populates="reviews_received")

    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='rating_check')
    )


class Message(Base):
    __table__ = "t_messages"

    id: Mapped[int] = mapped_column(primary_key=True)

    author: Mapped["User"] = relationship(back_populates="messages")
    ticket: Mapped["Ticket"] = relationship(back_populates="messages")

    content: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())


class Ticket(Base):
    __tablename__ = "t_reviews"

    id: Mapped[int] = mapped_column(primary_key=True)

    topicstarter: Mapped["User"] = relationship(back_populates="tickets")

    messages: Mapped[list["Message"]] = relationship(back_populates="ticket", cascade="all, delete-orphan")

    topic: Mapped[str] = mapped_column(nullable=False)
    commentary: Mapped[str] = mapped_column(nullable=False)