from pydantic import BaseModel
from datetime import datetime
from dataclasses import field
from typing import Optional
from uuid import UUID, uuid4

class Product_Model(BaseModel):
    id: Optional[UUID] = field(default_factory=uuid4)
    name: Optional[str] = ""
    description: Optional[str] = ""
    price: Optional[float]
    id_category: Optional[UUID]
    is_active: Optional[bool] = True
    createdAt: datetime = field(default_factory=datetime.now)
    updatedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None