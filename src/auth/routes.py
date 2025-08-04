
from fastapi import APIRouter, Depends , status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from datetime import timedelta, datetime
from src.db.main import get_session
from src.auth.schemas import UserCreateModel,UserModel,UserAddressModel
from src.auth.service import UserService
from src.errors import UserAlreadyExists
from src.auth.dependencies import AccessTokenBearer,RefreshTokenBearer,get_current_user
from src.auth.utils import verify_password,create_access_token

user_service = UserService()
access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()

auth_router = APIRouter()

REFRESH_TOKEN_EXPIRY = 2


@auth_router.post('/signup',response_model=UserModel,status_code=status.HTTP_201_CREATED)
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


@auth_router.get('/getByUID/{uid}')
async def get_user_ById(uid: str,session:AsyncSession=Depends(get_session)):
    user = await user_service.get_user_by_uid(uid,session)
    return user



@auth_router.post('/login')
async def login_user(login_data:UserCreateModel,
                     session:AsyncSession = Depends(get_session)):
    email = login_data.email
    phone_number = login_data.phone_number
    password = login_data.password

    user = await user_service.get_user(session,email,phone_number)

    if user is not None:
        password_valid = verify_password(password,user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={
                         "user_uid" :str(user.uid) ,
                         "role":user.role
                        }
                    )
            refresh_token = create_access_token(
                    user_data={
                         "user_uid" :str(user.uid) ,
                         "role":user.role
                        },      
                    refresh=True,
                    expiry= timedelta(days= REFRESH_TOKEN_EXPIRY)
                        )
            
            return JSONResponse(
                content={
                    'message': 'loging successful',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user':{
                        'uid': str(user.uid)
                    }
                }
            )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid Email or Password"
    )


@auth_router.get('/refresh_token') 
async def get_new_access_token(token_details: dict = Depends(refresh_token_bearer)):
    expiry_timestamp = token_details['exp']
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():

        new_access_token = create_access_token(
            user_data=token_details['user']
        )

        return JSONResponse(
            content={"access_token": new_access_token}
        )
    
    raise HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Invalid or expired token"
                    )


@auth_router.get('/me',response_model=UserAddressModel)
async def get_current_user(user = Depends(get_current_user)):
    return user

