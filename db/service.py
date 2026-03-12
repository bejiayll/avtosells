from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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

async def getAdsByFilters(session: AsyncSession, filter: AdFilterSchema, limit: int = 100, offset: int = 0) -> list[Ad]:
    res = await session.execute(select(Ad).where(
        Ad.millage in range(filter.min_milage, filter.min_milage) and
        Ad.volume in range(filter.min_volume, filter.max_volume) and
        Ad.price in range(filter.min_price, filter.max_price) and
        Ad.production_year in range(filter.min_year, filter.max_year) and
        Ad.horsepower in range(filter.min_power, filter.max_power) and
        (Ad.gearbox == filter.gearbox or filter.gearbox == 0) and 
        (Ad.drive == filter.drive or filter.drive == 0) and
        (Ad.form == filter.body_type or filter.body_type == 0)
    ).limit(limit).offset(offset).order_by(Ad.id))
    return res.scalars().all()

async def getThreadMessages(session: AsyncSession, ticket: Ticket) -> list[Message]: 
    res = await session.execute(select(Message).where(Message.ticket == ticket).order_by(Message.created_at))
    return res.scalar().all()

async def createUser(session: AsyncSession, s: UserSchema) -> User:
    user = User()
    user.email = s.email
    user.phone_number = s.phone_number
    user.password = s.password
    user.name = s.name
    user.tear = s.tear

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
