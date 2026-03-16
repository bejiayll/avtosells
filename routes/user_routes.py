from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from auth import security
from auth.service import current_user, require_permissions
from auth.schemamodels import SchemaUserResponse

from db import get_session
from db.models import *
from db.service import *

from application import app

from .social_schemas import *


@app.get("/me", response_model=SchemaUserResponse, dependencies=[Depends(require_permissions(0))])
async def protected(db: AsyncSession = Depends(get_session), user: User = Depends(current_user)):
    return user

@app.get("/admin", dependencies=[Depends(require_permissions(2))])
async def admin(db: AsyncSession = Depends(get_session), user: User = Depends(current_user)):
    return user 

adsRouter = APIRouter(prefix="/ad", tags=["ads"])
reviewsRouter = APIRouter(prefix="/review", tags=["review"], dependencies=[Depends(require_permissions(0))])
ticketRouter = APIRouter(prefix="/ticket", tags=["ticket"])

@adsRouter.get("/get/{id}", response_model=AdResponseSchema)
async def get_ad(id: int, session: AsyncSession = Depends(get_session)):
    
    ad = await getAdById(session, id)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    return ad

@adsRouter.post("/create", response_model=AdResponseSchema, status_code=201, dependencies=[Depends(require_permissions(0))])
async def create_ad(ad: AdCreateSchema, session: AsyncSession = Depends(get_session), user: User = Depends(current_user)):
    
    new_ad = Ad(**ad.model_dump(), author_id=user.id)
    
    session.add(new_ad)
    await session.commit()
    await session.refresh(new_ad)

    return new_ad

app.include_router(adsRouter)
app.include_router(reviewsRouter)
app.include_router(ticketRouter)