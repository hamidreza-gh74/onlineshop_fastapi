from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import Optional

from src.errors import UserNotFound,EmailOrPhoneNotExista
from src.auth.models import User
from src.auth.schemas import UserCreateModel
from src.auth.utils import generate_password_hash,verify_password


class UserService:
    
    async def get_user_by_uid(self,uid:str , session:AsyncSession):
        statement = select(User).where(User.uid == uid)
        result = await session.exec(statement)
        user = result.first()

        if user is not None:
            return user
        raise UserNotFound() 

    async def get_user_by_phoneNumber(self,phone_numnber:str , session:AsyncSession):
        statement = select(User).where(User.phone_number == phone_numnber)
        result = await session.exec(statement)
        user = result.first()

        return user
    
    async def get_user_by_email(self,email:str , session:AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()

        return user
    
    async def user_exists(self, session: AsyncSession, email: Optional[str], phone_number: Optional[str]) -> bool:
        if email is not None :
            user = await self.get_user_by_email(email, session)
        elif phone_number is not None :
            user = await self.get_user_by_phoneNumber(phone_number, session)
        else:
            raise EmailOrPhoneNotExista()

        return user is not None 
    
    async def get_user(self,session,email: Optional[str],phone_number:Optional[str]):
        if email is not None:
            user = await self.get_user_by_email(email,session)
        elif phone_number is not None:
            user = await self.get_user_by_phoneNumber(phone_number,session)
        else:
            raise EmailOrPhoneNotExista()
        
        if user is None:
            raise UserNotFound()
        
        return user

    
    async def create_user(self,
                          user_data:UserCreateModel,
                          session:AsyncSession):
        user_data_dict = user_data.model_dump()
        new_user = User(**user_data_dict)
        new_user.password_hash = generate_password_hash(user_data_dict["password"])
        new_user.role = "user"
        
        session.add(new_user)
        await session.commit()

        return new_user
    
    async def update_user(self,user:User ,user_data:dict, session:AsyncSession):
        for key,value in user_data.items():
            setattr(user,key,value)
            await session.commit()
            return user

