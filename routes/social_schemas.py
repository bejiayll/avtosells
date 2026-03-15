from enum import IntEnum
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional, List
from datetime import datetime


class Gearbox(IntEnum):
    G_MANUAL = 0
    G_AUTO = 1
    G_ROBOT = 2
    G_VARIATOR = 3

class Drive(IntEnum):
    DR_FRONT = 0
    DR_BACK = 1
    DR_FULL = 2

class Formfactor(IntEnum):
    FF_SEDAN = 0
    FF_HATCHBACK = 1
    FF_UNIVERSAL = 2
    FF_MICRO = 3
    FF_VAN = 4
    FF_MINIVAN = 5
    FF_CROSSOVER = 6
    FF_PICKUP = 7


class AdCreateSchema(BaseModel):
    brand: str
    price: int
    horsepower: float
    volume: float
    millage: int
    gearbox_steps: int
    gearbox: Gearbox
    drive: Drive
    form: Formfactor
    production_year: int
    images: List[str] = Field(default_factory=list)

class AdResponseSchema(BaseModel):
    id: int
    brand: str
    price: int
    horsepower: float
    volume: float
    millage: int
    gearbox_steps: int
    gearbox: Gearbox
    drive: Drive
    form: Formfactor
    production_year: int
    images: List[str]
    author_id: int
    created_at: datetime
    last_update: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class ReviewCreateSchema(BaseModel):
    content: str
    rating: int
    target_id: int

class ReviewResponseSchema(BaseModel):
    id: int
    content: str
    rating: int
    author_id: int
    target_id: int
    created_at: datetime
    last_update: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class MessageCreateSchema(BaseModel):
    content: str
    ticket_id: int

class MessageResponseSchema(BaseModel):
    id: int
    content: str
    author_id: int
    ticket_id: int
    created_at: datetime
    last_update: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class TicketCreateSchema(BaseModel):
    topic: str
    commentary: str

class TicketResponseSchema(BaseModel):
    id: int
    topic: str
    commentary: str
    topicstarter_id: int
    created_at: datetime
    last_update: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)