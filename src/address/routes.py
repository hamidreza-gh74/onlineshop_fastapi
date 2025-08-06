from fastapi import APIRouter, Depends,status
from sqlmodel import select,desc
from sqlmodel.ext.asyncio.session import AsyncSession
import uuid
from src.db.main import get_session
from src.address.models import Address
from src.address.schemas import AddressCreate,AddressUpdate
from src.auth.schemas import UserAddressModel
from src.auth.service import UserService
from src.auth.dependencies import AccessTokenBearer,get_current_user
from src.auth.schemas import UserAddressModel
from src.address.service import AddressService

user_service = UserService()
address_router = APIRouter()
access_token_bearer = AccessTokenBearer()
address_service = AddressService()



@address_router.post("/users/{user_uid}/addresses")    # create a address
async def add_address(user_uid: uuid.UUID, 
                      address_data: AddressCreate,
                      token_details:dict = Depends(access_token_bearer),
                      session: AsyncSession = Depends(get_session)):
     
     new_address = await address_service.create_address(user_uid,address_data,session)
     return new_address




@address_router.get('/user/allAddress/{user_uid}',response_model=list[Address])   # get all address for a user
async def get_all_address(user_uid:str,
                          token_details:dict = Depends(access_token_bearer),
                          session:AsyncSession=Depends(get_session)
                          ):
     
     addresses = await address_service.get_user_addresses(user_uid,session)
     return addresses
    



@address_router.get("/user/adresses",response_model=UserAddressModel)   # get user with all addresses
async def get_user_address(user = Depends(get_current_user)):  
      
      return user



@address_router.get("/{address_uid}")           # get a address by uid
async def get_a_address(address_uid:str,
                        token_details:dict = Depends(access_token_bearer),
                        session:AsyncSession=Depends(get_session)
                        ):
    address = await address_service.get_a_address(address_uid,session)
    return address




@address_router.patch('/{address_uid}',response_model=Address)  # update a address
async def update_address(address_uid:str, 
                      address_update_data:AddressUpdate,
                      token_details:dict = Depends(access_token_bearer),
                      session:AsyncSession=Depends(get_session)) -> dict:
    
    updated_address = await address_service.update_a_address(address_uid,address_update_data,session)
    return updated_address



@address_router.delete("/{address_uid}",status_code=status.HTTP_204_NO_CONTENT) #delete a address
async def delete_address(address_uid: str,
                         token_details:dict = Depends(access_token_bearer),
                         session:AsyncSession=Depends(get_session)
                      ):
    return await address_service.delete_a_address(address_uid,session)
    
  

@address_router.post("/set_default/{address_uid}")
async def set_default_address(address_uid: str,
                              token_details:dict = Depends(access_token_bearer),
                              session: AsyncSession = Depends(get_session)):
    # get a address
    address:Address = await address_service.get_a_address(address_uid,session)
   

    user_uid = address.user_uid

    #make all address false
    all_addresses = await address_service.get_user_addresses(user_uid,session)
    for addr in all_addresses:
        addr.is_default = False
        session.add(addr)

    # change this address to true
    address.is_default = True
    session.add(address)

    await session.commit()
    return {"message": "Default address set successfully"}


      
      


    
    
    



