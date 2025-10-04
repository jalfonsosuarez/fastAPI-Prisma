from pydantic import BaseModel
from datetime import datetime
from dataclasses import field
from typing import Optional
from uuid import UUID, uuid4

class Product_Model(BaseModel):
    id: Optional[UUID] = field(default_factory=uuid4)
    name: str
    description: str
    price: float
    id_category: UUID
    is_active: Optional[bool] = True
    createdAt: datetime = field(default_factory=datetime.now)
    updatedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None
class Product_Model_Update(Product_Model):
    name: Optional[str] = "" # type: ignore
    description: Optional[str] = "" # type: ignore
    price: Optional[float] # type: ignore
    id_category: Optional[UUID]=None # type: ignore
    is_active: Optional[bool] = True
    createdAt: datetime = field(default_factory=datetime.now)
    updatedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None