from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from prisma import Prisma

from utils.auth_utils import is_admin
from .models.category_model import Category_Model
from uuid import UUID
from datetime import datetime
from utils.encrypt import get_password_hash

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

categoryAPI = APIRouter(
    tags=['Categories']
)

db = Prisma()

@categoryAPI.get("/categories")
async def get_all_categories(token: str = Depends(oauth2_scheme)):
    await db.connect()
    categories = await db.category.find_many(where={'is_active': True})
    await db.disconnect()
    return categories

@categoryAPI.get("/categories/{id_category}")
async def get_user(id_category: UUID, token: str= Depends(oauth2_scheme)):
    await db.connect()
    category = await db.category.find_first(where={'id': str(id_category)})
    await db.disconnect()
    return category

@categoryAPI.post("/categories")
async def save_category(category: Category_Model, token: str= Depends(oauth2_scheme)):
    if not is_admin(token):
        raise HTTPException(status_code=401, detail="No tienes permisos para acceder.")
    
    await db.connect()
    post = await db.category.create(
        data={
            "description": str(category.description),
        }
    )
    await db.disconnect()
    return post

@categoryAPI.put("/categories/{id_category}")
async def update_user(id_category: UUID, data: Category_Model, token: str= Depends(oauth2_scheme)):
    if not is_admin(token):
        raise HTTPException(status_code=401, detail="No tienes permisos para acceder.")
    
    await db.connect()
    update_data = data.model_dump(exclude_unset=True)
    category = await db.category.update(
        where={"id": str(id_category)},
        data=update_data # type: ignore
    )
    await db.disconnect()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@categoryAPI.delete("/category/{id_category}")
async def delete_user(id_category: UUID,  token: str= Depends(oauth2_scheme)):
    if not is_admin(token):
        raise HTTPException(status_code=401, detail="No tienes permisos para acceder.")
    
    await db.connect()
    category = await db.category.update(
        where={"id": str(id_category)},
        data={
            "is_active": False,
            "deletedAt": datetime.now()
        }
    )
    await db.disconnect()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
