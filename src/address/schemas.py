
from sqlmodel import SQLModel
from typing import  Optional



class AddressBase(SQLModel):
    title: str
    province: str
    city: str
    postal_code: str
    full_address: str
    phone_number: str
    is_default: bool = False

    

class AddressCreate(AddressBase):
    
    class Config:
        from_attributes = True


class AddressUpdate(SQLModel):
    title: Optional[str]
    province: Optional[str]
    city: Optional[str]
    postal_code: Optional[str]
    full_address: Optional[str]
    phone_number: Optional[str]
