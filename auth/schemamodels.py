from pydantic import BaseModel, EmailStr
from typing import Optional

class SchemaUserLogin(BaseModel):
    email: str = EmailStr()
    password: str

class SchemaUserRegister(BaseModel):
    username: str
    name: str
    email: str = EmailStr()
    phone: str
    password: str

class SchemaUserResponse(BaseModel):
    id: int
    email: str
    name: str
    phone: Optional[str] = None
    
    class Config:
        from_attributes = True