from typing import Optional
from core.model.zero_model import ZeroModel
from sqlmodel import Field,Relationship
import uuid

class Addreess(ZeroModel, table = True):

    __tablename__ = "addresses"
    user_uid: Optional[uuid.UUID] = Field(default=None,foreign_key='users.uid')
    title: str
    province: str 
    city: str 
    full_address: str
    postal_code: str
    phone: str
    is_default: bool

    user:Optional['User'] = Relationship(back_populates="addressers",sa_relationship_kwargs={"lazy":"selectin"})

    

from src.auth.models import User
