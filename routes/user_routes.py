from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from auth import security
from auth.service import current_user, require_permissions
from auth.schemamodels import SchemaUserResponse

from db import get_session
from db.models import *
from db.service import *
from db.schemamodels import AdFilterSchema

from application import app

from .social_schemas import *


adsRouter = APIRouter(prefix="/ad", tags=["ads"])
userRouter = APIRouter(prefix="/user", tags=["user"])
ticketRouter = APIRouter(prefix="/ticket", tags=["ticket"])
reviewRouter = APIRouter(prefix="/review", tags=["review"])

@app.get("/me", response_model=SchemaUserResponse, dependencies=[Depends(require_permissions(0))])
async def protected(user: User = Depends(current_user)):
    return user

@app.get("/user/{id}", response_model=SchemaUserResponse, dependencies=[Depends(require_permissions(-1))])
async def get_user(id: int, session: AsyncSession = Depends(get_session), user: User = Depends(current_user)):
    _user = getUserById(session, id)
    if not _user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return _user

@adsRouter.get("/get/{id}", response_model=AdResponseSchema)
async def get_ad(id: int, session: AsyncSession = Depends(get_session)):
    
    ad = await getAdById(session, id)
    if not ad:
        raise HTTPException(status_code=404, detail="Объявление не найдено")
    return ad

@adsRouter.post("/create", response_model=AdResponseSchema, status_code=201, dependencies=[Depends(require_permissions(0))])
async def create_ad(ad: AdCreateSchema, session: AsyncSession = Depends(get_session), user: User = Depends(current_user)):
    new_ad = Ad(**ad.model_dump(), author_id=user.id)
    
    session.add(new_ad)
    await session.commit()
    await session.refresh(new_ad)

    return new_ad

@adsRouter.get("/", response_model=list[AdResponseSchema])
async def get_ads(filters: AdFilterSchema = Depends(parse_ad_filters), session: AsyncSession = Depends(get_session)):
    ads = await getAdsByFilters(session, filters)
    return ads


@ticketRouter.post("/create", response_model=TicketResponseSchema, status_code=201, dependencies=[Depends(require_permissions(-1))])
async def create_ticket(_ticket: TicketCreateSchema, session: AsyncSession = Depends(get_session), user: User = Depends(current_user)):
    new_ticket = Ticket(
        **_ticket.model_dump(),
        topicstarter_id=user.id
    )
    session.add(new_ticket)
    await session.commit()
    await session.refresh(new_ticket)
    return new_ticket



@ticketRouter.get("/get/{id}", response_model=TicketResponseSchema)
async def get_ticket(id: int, session: AsyncSession = Depends(get_session), user: User = Depends(current_user)):
    result = await session.execute(
        select(Ticket)
        .options(selectinload(Ticket.messages))  
        .where(Ticket.id == id)
    )
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Тикет не найден")
    
    if user.tear < 1 and ticket.topicstarter_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав"
        )
    
    ticket.messages.sort(key=lambda m: m.created_at)
    
    return ticket


@ticketRouter.post("/message", response_model=MessageResponseSchema, status_code=201)
async def send_message(message: MessageCreateSchema, session: AsyncSession = Depends(get_session), user: User = Depends(current_user)):
    result = await session.execute(
        select(Ticket).where(Ticket.id == message.ticket_id)
    )
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Тикет не найден")

    if user.tier < 1 and ticket.topicstarter_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для общения в этом тикете"
        )
    
    new_message = Message(
        **message.model_dump(),
        author_id=user.id
    )
    session.add(new_message)
    await session.commit()
    await session.refresh(new_message)
    
    return new_message

@reviewRouter.post("/create", response_model=ReviewResponseSchema, status_code=201, dependencies=[Depends(require_permissions(0))])
async def create_review(review: ReviewCreateSchema, session: AsyncSession = Depends(get_session), user: User = Depends(current_user)):
    target = await session.get(User, review.target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Цель не найдена")

    if target.id == user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя оставлять отзыв на себя"
        )
    
    new_review = Review(
        **review.model_dump(),
        author_id=user.id
    )
    session.add(new_review)
    await session.commit()
    await session.refresh(new_review)
    
    return new_review


@reviewRouter.get("/get/{id}", response_model=ReviewResponseSchema, dependencies=[Depends(require_permissions(0))])
async def get_review(id: int, session: AsyncSession = Depends(get_session), user: User = Depends(current_user)):
    review = await session.get(Review, id)
    
    if not review:
        raise HTTPException(status_code=404, detail="Отзыв не найден")
    
    return review

app.include_router(adsRouter)
app.include_router(reviewRouter)
app.include_router(ticketRouter)
app.include_router(userRouter)