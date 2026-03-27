from __future__ import annotations

from datetime import datetime

from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import DateTime, func, ForeignKey, String, CheckConstraint, Integer, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase): ...

class User(Base):
    __tablename__ = "t_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    last_update: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    tier: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    reviews_sent: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="author",
        foreign_keys="[Review.author_id]",  
        cascade="all, delete-orphan"
    )
    reviews_received: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="target",
        foreign_keys="[Review.target_id]",  
        cascade="all, delete-orphan"
    )

    ads: Mapped[list["Ad"]] = relationship("Ad", back_populates="author", cascade="all, delete-orphan")
    tickets: Mapped[list["Ticket"]] = relationship("Ticket", back_populates="topicstarter")
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="author")


class Ad(Base):
    __tablename__ = "t_ads"

    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    horsepower: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[float] = mapped_column(Float, nullable=False)
    millage: Mapped[int] = mapped_column(Integer, nullable=False)
    gearbox_steps: Mapped[int] = mapped_column(Integer, nullable=False)
    gearbox: Mapped[int] = mapped_column(Integer, nullable=False)
    drive: Mapped[int] = mapped_column(Integer, nullable=False)
    form: Mapped[int] = mapped_column(Integer, nullable=False)
    production_year: Mapped[int] = mapped_column(Integer, nullable=False)
    images: Mapped[list[str]] = mapped_column(ARRAY(String))
    
    author_id: Mapped[int] = mapped_column(ForeignKey("t_users.id"), nullable=False, index=True)
    author: Mapped["User"] = relationship("User", back_populates="ads")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    __table_args__ = (CheckConstraint('production_year >= 1945', name='year_limit'),)


class Review(Base):
    __tablename__ = "t_reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    author_id: Mapped[int] = mapped_column(ForeignKey("t_users.id"), nullable=False)
    target_id: Mapped[int] = mapped_column(ForeignKey("t_users.id"), nullable=False)

    author: Mapped["User"] = relationship(
        "User",
        back_populates="reviews_sent",
        foreign_keys=[author_id]
    )
    target: Mapped["User"] = relationship(
        "User",
        back_populates="reviews_received",
        foreign_keys=[target_id] 
    )

    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='rating_check'),
    )


class Message(Base):
    __tablename__ = "t_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    author_id: Mapped[int] = mapped_column(ForeignKey("t_users.id"), nullable=False, index=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("t_tickets.id"), nullable=False, index=True)
    
    content: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    
    author: Mapped["User"] = relationship("User", back_populates="messages")
    ticket: Mapped["Ticket"] = relationship("Ticket", back_populates="messages")


class Ticket(Base):
    __tablename__ = "t_tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    topicstarter_id: Mapped[int] = mapped_column(ForeignKey("t_users.id"), nullable=False, index=True)
    topicstarter: Mapped["User"] = relationship("User", back_populates="tickets")
    
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="ticket", cascade="all, delete-orphan")
    
    topic: Mapped[str] = mapped_column(String(255), nullable=False)
    commentary: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    last_update: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=True)