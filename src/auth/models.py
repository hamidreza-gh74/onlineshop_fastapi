from core.model.zero_model import ZeroModel
from sqlmodel import SQLModel
from sqlmodel import Field,Column ,Relationship
from datetime import date
from typing import Optional
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime,timedelta
import uuid
from sqlalchemy import func



class User(ZeroModel, table = True):
    __tablename__ = "users"

    first_name: Optional[str] 
    last_name: Optional[str]
    gender: Optional[str]
    birthday: Optional[date]
    username: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    password_hash: Optional[str] = Field(exclude=True)
    is_verifed: Optional[bool] = Field(default=False)
    role:str = Field(
        sa_column=Column(pg.VARCHAR,nullable=False,server_default="user")
        )
    
    addresses:list['Address'] = Relationship(back_populates="user",sa_relationship_kwargs={"lazy":"selectin"})
    codes: list["VerificationCode"] = Relationship(back_populates="user")
    refresh_tokens: list["RefreshToken"] = Relationship(back_populates="user")


from src.address.models import Address




class VerificationCode(SQLModel, table=True):
    __tablename__ = "verification"
    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True
    )
    user_id: uuid.UUID = Field(foreign_key="users.uid")
    code: str
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"server_default": func.now()}
                                    )
    expires_at: datetime = Field(default_factory=lambda: datetime.now() + timedelta(minutes=2))
   

    user: Optional["User"] = Relationship(back_populates="codes")


    
class RefreshToken(SQLModel, table=True):
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    user_id: uuid.UUID = Field(foreign_key="users.uid")
    refresh_token: str = Field(index=True, unique=True)
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.now)
    is_revoked: bool = Field(default=False)

    user: Optional["User"] = Relationship(back_populates="refresh_tokens")




























