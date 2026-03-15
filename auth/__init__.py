import os
from dotenv import load_dotenv

from fastapi import HTTPException, Response, Depends, status
from authx import AuthX, AuthXConfig

from bcrypt import checkpw, hashpw, gensalt

from application import app
from .schemamodels import SchemaUserLogin, SchemaUserRegister

from db import get_session
from db.models import *
from db.service import *
from db.schemamodels import UserSchema

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
async def login(creds: SchemaUserLogin, response: Response, session: AsyncSession = Depends(get_session)):

    user = await getUserByEmail(session, creds.email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not checkpw(creds.password.encode("utf-8"), user.password.encode("utf-8")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )        

    token = security.create_access_token(uid=str(user.id))
    response.set_cookie(
        key=config.JWT_ACCESS_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax"
    )
    return {"access_token": token}


@app.post("/registration")
async def register(creds: SchemaUserRegister, response: Response, session: AsyncSession = Depends(get_session)):
    
    user = await getUserByEmail(session, creds.email)

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user = User(**creds.model_dump)
    session.add(user)
    await session.commit()
    await session.refresh()

    token = security.create_access_token(uid=str(user.id))
    response.set_cookie(
        key=config.JWT_ACCESS_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax"
    )

    return {"access_token": token}

# @app.post("/protected")
# def protected(user=Depends(security.access_token_required)):
#     return {'msg': 'private info'}