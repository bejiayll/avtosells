from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from authx import AuthX, TokenPayload
from authx.exceptions import AuthXException
from jose import JWTError

from db.models import *
from db.service import *
from db import get_session

from . import config, security


async def get_token(request: Request) -> str:
    token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
    return token

async def current_user(request: Request, db: AsyncSession = Depends(get_session)) -> User:
    token = await get_token(request)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    try:
        payload: TokenPayload = security._decode_token(token)
        user_id = int(payload.sub)
        
    except AuthXException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if payload.type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )


    user = await getUserById(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User doesn't exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

def require_permissions(tier: int):
    """
        @router.get("/admin", dependencies=[Depends(require_permissions(x))])
        async def admin_panel(current_user: User = Depends(current_user)):
            ...
    """
    async def check_tear(current_user: User = Depends(current_user)):
        if current_user.tier < tier:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Недостаточно прав."
            )
        return current_user
    
    return check_tear