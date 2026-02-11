from pydantic import BaseModel, EmailStr

class SchemaUserLogin(BaseModel):
    email: str = EmailStr()
    password: str

class SchemaUserRegister(BaseModel):
    username: str
    name: str
    email: str = EmailStr()
    phone: str
    password: str

