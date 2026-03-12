from pydantic import BaseModel, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
import phonenumbers
from typing import Annotated

from datetime import date


PhoneNumber.default_region = 'RU'

class AdFilterSchema(BaseModel):
    max_milage: int = 1000000000
    min_milage: int = 1 

    max_volume: float = 170.0
    min_volume: float = 0.8

    max_price: int = 50000000
    min_price: int = 1000

    max_year: int = int(date.today().year)
    min_year: int = 1945

    max_power: int = 1000
    min_power: int = 1

    gearbox: int = 0
    drive: int = 0
    body_type: int = 0

class UserSchema(BaseModel):
    email: EmailStr
    phone_number: Annotated[str, PhoneNumber]
    password: str
    name: str
    tear: int = 0