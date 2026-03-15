from pydantic import BaseModel, EmailStr, ConfigDict
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
    phone_number: Optional[str] = None
    tear: int
    
    model_config = ConfigDict(from_attributes=True)