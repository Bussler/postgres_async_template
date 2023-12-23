from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

user_router = APIRouter(prefix='/user', tags=['user'])

@user_router.get('')
async def get():
    return {'user': 'user'}

@user_router.get('/greeting')
async def greeting():
    return {'greeting': 'Hello, user!'}