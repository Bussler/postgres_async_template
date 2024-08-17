from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.user.schema import UserSchema
from app.db import AsyncSession, get_session
from app.db.models.model_export import DBUser

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("", response_model=List[UserSchema])
async def get(
    name: Optional[str] = None,
    surname: Optional[str] = None,
    limit: int = 100,
    db_session: AsyncSession = Depends(get_session),
) -> List[UserSchema]:
    stmt = select(DBUser)

    if name:
        stmt = stmt.where(DBUser.name == name)

    if surname:
        stmt = stmt.where(DBUser.surname == surname)

    users = await db_session.scalars(stmt.limit(limit))
    users_list = list(users)

    return [UserSchema.model_validate(user) for user in users_list]


@user_router.post("/create")
async def create(
    name: str,
    surname: str,
    db_session: AsyncSession = Depends(get_session),
) -> UserSchema:
    user = await db_session.scalar(
        select(DBUser).where(DBUser.name == name).where(DBUser.surname == surname)
    )

    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User already exists",
        )

    new_user = DBUser(name=name, surname=surname)

    db_session.add(new_user)
    await db_session.commit()
    await db_session.refresh(new_user)

    return UserSchema.model_validate(new_user)


@user_router.get("/greeting")
async def greeting():
    return {"greeting": "Hello, user!"}
