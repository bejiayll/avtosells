import os
from dotenv import load_dotenv

from fastapi import HTTPException, Response, Depends
from authx import AuthX, AuthXConfig

from application import app
from .schemamodels import SchemaUserLogin, SchemaUserRegister

load_dotenv()

config = AuthXConfig(
    JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
    JWT_ACCESS_COOKIE_NAME="avtosells_access_token",
    JWT_TOKEN_LOCATION=["cookies"],
    JWT_COOKIE_CSRF_PROTECT=False,
    JWT_COOKIE_SECURE=False
)

security = AuthX(config=config) 

@app.post("/login")
def login(creds: SchemaUserLogin, response: Response):
    if creds.email == "test@example.com" and creds.password == "test":
        token = security.create_access_token(uid="12345")
        response.set_cookie(
            key=config.JWT_ACCESS_COOKIE_NAME,
            value=token,
            httponly=True,
            samesite="lax"
        )
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Incorrect username or password")


@app.post("/registration")
def register(cred: SchemaUserRegister):
    ...

@app.post("/protected")
def protected(user=Depends(security.access_token_required)):
    return {'msg': 'private info'}