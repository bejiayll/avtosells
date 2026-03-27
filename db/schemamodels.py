from pydantic import BaseModel, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
import phonenumbers

from typing import Annotated, Optional

from datetime import date

PhoneNumber.default_region = 'RU'

class AdFilterSchema(BaseModel):
    min_millage: Optional[int] = Field(None, ge=0)
    max_millage: Optional[int] = Field(None, ge=0)
    
    min_volume: Optional[float] = Field(None, gt=0)
    max_volume: Optional[float] = Field(None, gt=0)
    
    min_price: Optional[int] = Field(None, ge=0)
    max_price: Optional[int] = Field(None, ge=0)
    
    min_year: Optional[int] = Field(None, ge=1945, le=2100)
    max_year: Optional[int] = Field(None, ge=1945, le=2100)
    
    min_power: Optional[int] = Field(None, ge=0)
    max_power: Optional[int] = Field(None, ge=0)
    
    gearbox: Optional[int] = Field(None, ge=0, le=3)
    drive: Optional[int] = Field(None, ge=0, le=2)
    body_type: Optional[int] = Field(None, ge=0, le=7)
    
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

class UserSchema(BaseModel):
    email: EmailStr
    phone_number: Annotated[str, PhoneNumber]
    password: str
    name: str
    tier: int = 0