from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth import security
from auth.service import current_user
from auth.schemamodels import SchemaUserResponse

from db import get_session
from db.models import *
from db.service import *

from application import app

@app.get("/me", response_model=SchemaUserResponse)
def protected(db: AsyncSession = Depends(get_session), user: User = Depends(current_user)):
    return user