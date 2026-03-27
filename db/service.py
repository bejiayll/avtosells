from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Query
from typing import Optional

from .models import *
from .schemamodels import *

async def getUserById(session: AsyncSession, id: int) -> User:
    res = await session.execute(select(User).where(User.id == id))
    return res.scalar_one_or_none()

async def getUserByEmail(session: AsyncSession, email: str) -> User:
    res = await session.execute(select(User).where(User.email == email))
    return res.scalar_one_or_none()

async def getAdById(session: AsyncSession, id: int) -> Ad:
    res = await session.execute(select(Ad).where(Ad.id == id))
    return res.scalar_one_or_none()

async def getAdsByFilters(
    session: AsyncSession, 
    filters: AdFilterSchema
) -> list[Ad]:
    query = select(Ad)
    
    conditions = []
    
    if filters.min_millage is not None:
        conditions.append(Ad.millage >= filters.min_millage)
    if filters.max_millage is not None:
        conditions.append(Ad.millage <= filters.max_millage)
    
    if filters.min_volume is not None:
        conditions.append(Ad.volume >= filters.min_volume)
    if filters.max_volume is not None:
        conditions.append(Ad.volume <= filters.max_volume)
    
    if filters.min_price is not None:
        conditions.append(Ad.price >= filters.min_price)
    if filters.max_price is not None:
        conditions.append(Ad.price <= filters.max_price)
    
    if filters.min_year is not None:
        conditions.append(Ad.production_year >= filters.min_year)
    if filters.max_year is not None:
        conditions.append(Ad.production_year <= filters.max_year)
    
    if filters.min_power is not None:
        conditions.append(Ad.horsepower >= filters.min_power)
    if filters.max_power is not None:
        conditions.append(Ad.horsepower <= filters.max_power)
    
    if filters.gearbox not in (None, 0):
        conditions.append(Ad.gearbox == filters.gearbox)
    if filters.drive not in (None, 0):
        conditions.append(Ad.drive == filters.drive)
    if filters.body_type not in (None, 0):
        conditions.append(Ad.form == filters.body_type)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    query = query.order_by(Ad.created_at.desc())
    
    query = query.offset(filters.offset).limit(filters.limit)
    
    result = await session.execute(query)
    return result.scalars().all()

async def getThreadMessages(session: AsyncSession, ticket: Ticket) -> list[Message]: 
    res = await session.execute(select(Message).where(Message.ticket == ticket).order_by(Message.created_at))
    return res.scalar().all()

async def createUser(session: AsyncSession, s: UserSchema) -> User:
    user = User()
    user.email = s.email
    user.phone_number = s.phone_number
    user.password = s.password
    user.name = s.name
    user.tear = s.tier

    session.add(user)
    await session.commit()

    return user

async def updateUser(session: AsyncSession, id: int, s: UserSchema) -> User:
    user = getUserById(session, id)
    user.email = s.email
    user.phone_number = s.phone_number
    user.password = s.password
    user.name = s.name
    user.tear = s.tear
    
    await session.commit()
    
    return user

def parse_ad_filters(
    min_millage: Optional[int] = Query(None, ge=0),
    max_millage: Optional[int] = Query(None, ge=0),
    min_volume: Optional[float] = Query(None, gt=0),
    max_volume: Optional[float] = Query(None, gt=0),
    min_price: Optional[int] = Query(None, ge=0),
    max_price: Optional[int] = Query(None, ge=0),
    min_year: Optional[int] = Query(None, ge=1945, le=2100),
    max_year: Optional[int] = Query(None, ge=1945, le=2100),
    min_power: Optional[int] = Query(None, ge=0),
    max_power: Optional[int] = Query(None, ge=0),
    gearbox: Optional[int] = Query(None, ge=0, le=3),
    drive: Optional[int] = Query(None, ge=0, le=2),
    body_type: Optional[int] = Query(None, ge=0, le=7),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> AdFilterSchema:
    return AdFilterSchema(
        min_millage=min_millage,
        max_millage=max_millage,
        min_volume=min_volume,
        max_volume=max_volume,
        min_price=min_price,
        max_price=max_price,
        min_year=min_year,
        max_year=max_year,
        min_power=min_power,
        max_power=max_power,
        gearbox=gearbox,
        drive=drive,
        body_type=body_type,
        limit=limit,
        offset=offset
    )