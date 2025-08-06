
from sqlmodel import select,desc
from sqlmodel.ext.asyncio.session import AsyncSession
from src.address.models import Address
import uuid
from src.address.schemas import AddressCreate,AddressUpdate
from src.errors import AddressNotFound


class AddressService:

    async def get_a_address(self, address_uid: str, session: AsyncSession):
        statement = select(Address).where(address_uid == Address.uid)
        result = await session.exec(statement)
        address = result.first()

        if address is not None:
            return address
        raise AddressNotFound()

    


    async def get_user_addresses(self, user_uid:str, session: AsyncSession):

        statement = (
            select(Address)
            .where(Address.user_uid == user_uid)
            .order_by(desc(Address.created_at))
        )
        address = await session.exec(statement)

        if address is not None:
            return address.all()
        raise AddressNotFound()
        



    async def create_address( self,
                            user_uid: uuid.UUID, 
                            address_data: AddressCreate,
                            session:AsyncSession
        ):
         
        address_data_dict = address_data.model_dump()
        address = Address(**address_data_dict, user_uid=user_uid)
        session.add(address)
        await session.commit()
        await session.refresh(address)
        return address
    


    async def update_a_address(
                                self, 
                                address_uid: str, 
                                update_data: AddressUpdate, 
                                session: AsyncSession):
        
        address_to_update = await self.get_a_address(address_uid, session)

        if address_to_update is not None:
            update_data_dict = update_data.model_dump()

            for key, value in update_data_dict.items():
                setattr(address_to_update, key, value)

            await session.commit()
            return address_to_update

        raise AddressNotFound()
    

    async def delete_a_address(self,
                           address_uid: str, 
                           session: AsyncSession
                           ):
        
        address_to_delete = await self.get_a_address(address_uid, session)

        if address_to_delete is not None:
            await session.delete(address_to_delete)
            await session.commit()
            return {"message": "the book has been deleted"}

        raise AddressNotFound()


