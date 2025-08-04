from sqlmodel import SQLModel
from typing import Optional
from  datetime import datetime, date
from sqlmodel import Field
import uuid
from pydantic import model_validator
from src.errors import EmailOrPhoneNotExista



class UserCreateModel(SQLModel):
    phone_number: Optional[str]
    email: Optional[str]
    password:str

    @model_validator(mode="after")
    def check_email_or_phone(cls, values):
        if not values.email and not values.phone_number:
            raise EmailOrPhoneNotExista()
        return values
    
class UserModel(SQLModel):
    uid: uuid.UUID 
    first_name: Optional[str] 
    last_name: Optional[str]
    gender: Optional[str]
    birthday: Optional[date]
    username: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    hash_password: Optional[str] = Field(exclude=True)
    is_verifed: Optional[bool] = Field(default=False)
    role:str 
    created_at: datetime 
    updated_at: datetime 



class UserAddressModel(UserModel):
    addressers:Optional['Addreess'] 


class UserLoginModel(SQLModel):
    email:str = Field(max_length=40)
    password:str = Field(min_length=6)



class PasswordResetModel(SQLModel):
     email:str

class PasswordResetConfirmModel(SQLModel):
     new_password: str
     confirm_password: str


from src.address.models import Addreess