from sqlmodel import SQLModel
import uuid
from typing import Optional

class CategoryBase(SQLModel):
    name: str
    image_url: Optional[str] = None
    parent_uid: Optional[uuid.UUID] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    uid: uuid.UUID
    depth: int

    class Config:
        orm_mode = True


class CategoryUpdate(SQLModel):
    name: Optional[str] = None
    image_url: Optional[str] = None
    parent_uid: Optional[uuid.UUID] = None

