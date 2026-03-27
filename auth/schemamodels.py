from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

class SchemaUserLogin(BaseModel):
    email: str = EmailStr()
    password: str

class SchemaUserRegister(BaseModel):
    name: str
    email: str = EmailStr()
    phone_number: str
    password: str

class SchemaUserResponse(BaseModel):
    id: int
    email: str
    name: str
    phone_number: Optional[str] = None
    created_at: datetime 
    tier: int
    
    model_config = ConfigDict(from_attributes=True)