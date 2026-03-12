import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .models import *

from application import app

load_dotenv()

database_url = os.environ.get("DATABASE_URL")

engine = create_async_engine(
    database_url, 
    echo=True,
)

session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with session() as new_session: 
        yield new_session

@app.on_event("startup")
async def setup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    