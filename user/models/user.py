from pydantic import BaseModel
from datetime import datetime
from dataclasses import field
from typing import Optional
from uuid import UUID, uuid4

class User(BaseModel):
    id: Optional[UUID] = field(default_factory=uuid4)
    fullname: Optional[str] = ""
    email: Optional[str] = ""
    role: Optional[str] = "USER"
    password: Optional[str] = ""
    is_active: Optional[bool] = True
    createdAt: datetime = field(default_factory=datetime.now)
    updatedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None
