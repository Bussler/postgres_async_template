from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db import AsyncSession, get_session

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("")
async def get(
    name: Optional[str] = None,
    surname: Optional[str] = None,
    db_session: AsyncSession = Depends(get_session),
):
    return {"user": "user"}


@user_router.get("/greeting")
async def greeting():
    return {"greeting": "Hello, user!"}
