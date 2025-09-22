from fastapi import APIRouter, HTTPException
import asyncio
from prisma import Prisma
from .models.user import User
from uuid import UUID
from datetime import datetime
from  utils.encrypt import get_password_hash


userAPI = APIRouter(
    tags=['Users']
)

db = Prisma()

@userAPI.get("/users")
async def get_all_users():
    await db.connect()
    users = await db.user.find_many()
    for user in users:
        if hasattr(user, 'password'):
            user.password = '****'
    await db.disconnect()
    return users

@userAPI.get("/users/{id_user}")
async def get_user(id_user: UUID):
    await db.connect()
    user = await db.user.find_first(where={'id': str(id_user)})
    await db.disconnect()
    if user:
        user.password = '****'
    return user

@userAPI.post("/users")
async def save_user(user: User):
    password = get_password_hash(str(user.password))
    await db.connect()
    post = await db.user.create(
        data={
            "fullname": str(user.fullname),
            "email": str(user.email),
            "role": str(user.role),
            "password": password,
            "is_active": bool(user.is_active)
        }
    )
    post.password = '****'
    await db.disconnect()
    return post

@userAPI.put("/users/{id_user}")
async def update_user(id_user: UUID, data: User):
    await db.connect()
    update_data = data.model_dump(exclude_unset=True)
    user = await db.user.update(
        where={"id": str(id_user)},
        data=update_data # type: ignore
    )
    await db.disconnect()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if hasattr(user, 'password'):
        user.password = '****'
    return user

@userAPI.delete("/users/{id_user}")
async def delete_user(id_user: UUID):
    await db.connect()
    user = await db.user.update(
        where={"id": str(id_user)},
        data={
            "is_active": False,
            "deletedAt": datetime.now()
        }
    )
    await db.disconnect()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if hasattr(user, 'password'):
        user.password = '****'
    return user