from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from prisma import Prisma

from utils.auth_utils import is_admin
from .models.product_model import Product_Model
from uuid import UUID
from datetime import datetime

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

productAPI = APIRouter(
    tags=['Products']
)

db = Prisma()

@productAPI.get("/products")
async def get_all_products(token: str = Depends(oauth2_scheme)):
    await db.connect()
    categories = await db.product.find_many(where={'is_active': True})
    await db.disconnect()
    return categories

@productAPI.get("/products/{id_product}")
async def get_user(id_product: UUID, token: str= Depends(oauth2_scheme)):
    await db.connect()
    product = await db.product.find_first(where={'id': str(id_product)})
    await db.disconnect()
    return product

@productAPI.post("/products")
async def save_category(product: Product_Model, token: str= Depends(oauth2_scheme)):
    if not is_admin(token):
        raise HTTPException(status_code=401, detail="No tienes permisos para acceder.")
    
    await db.connect()
    post = await db.product.create(
        data={
            "name": str(product.name),
            "description": str(product.description),
            "price": product.price, # type: ignore
            "id_category": str(product.id_category)
        }
    )
    await db.disconnect()
    return post

@productAPI.put("/products/{id_category}")
async def update_user(id_product: UUID, data: Product_Model, token: str= Depends(oauth2_scheme)):
    if not is_admin(token):
        raise HTTPException(status_code=401, detail="No tienes permisos para acceder.")
    
    await db.connect()
    update_data = data.model_dump(exclude_unset=True)
    product = await db.product.update(
        where={"id": str(id_product)},
        data=update_data # type: ignore
    )
    await db.disconnect()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@productAPI.delete("/products/{id_product}")
async def delete_user(id_product: UUID,  token: str= Depends(oauth2_scheme)):
    if not is_admin(token):
        raise HTTPException(status_code=401, detail="No tienes permisos para acceder.")
    
    await db.connect()
    product = await db.product.update(
        where={"id": str(id_product)},
        data={
            "is_active": False,
            "deletedAt": datetime.now()
        }
    )
    await db.disconnect()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
