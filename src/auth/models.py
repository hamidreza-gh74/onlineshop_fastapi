from core.model.zero_model import ZeroModel
from sqlmodel import Field,Column ,Relationship
from datetime import date
from typing import Optional
import sqlalchemy.dialects.postgresql as pg


class User(ZeroModel, table = True):
    __tablename__ = "users"

    first_name: Optional[str] 
    last_name: Optional[str]
    gender: Optional[str]
    birthday: Optional[date]
    username: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    hash_password: Optional[str] = Field(exclude=True)
    is_verifed: Optional[bool] = Field(default=False)
    role:str = Field(
        sa_column=Column(pg.VARCHAR,nullable=False,server_default="user")
        )
    
    addressers:Optional['Addreess'] = Relationship(back_populates="user",sa_relationship_kwargs={"lazy":"selectin"})


from src.address.models import Addreess

    

