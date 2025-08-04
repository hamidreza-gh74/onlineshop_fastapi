
from fastapi import APIRouter, Depends , status
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from src.db.main import get_session
from src.auth.schemas import UserCreateModel
from src.auth.service import UserService
from src.errors import UserAlreadyExists

user_service = UserService()

auth_router = APIRouter()

@auth_router.post('/signup',response_model=UserCreateModel,status_code=status.HTTP_201_CREATED)
async def create_user(user_data:UserCreateModel,
                      session:AsyncSession = Depends(get_session),
                      ):
    email = user_data.email
    phone_number = user_data.phone_number

    user_exists = await user_service.user_exists(session,email,phone_number)

    if user_exists:
        raise UserAlreadyExists()

  
    new_user = await user_service.create_user(user_data,session)
 
    return new_user


@auth_router.get('/getByUID')
async def get_user_ById(uid: str,session:AsyncSession=Depends(get_session)):
    user = await user_service.get_user_by_uid(uid,session)



    