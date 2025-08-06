from fastapi import APIRouter, Depends , status, Header
from sqlmodel import select
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from datetime import timedelta, datetime
from src.db.main import get_session
from src.auth.schemas import UserCreateModel,UserModel,UserAddressModel
from src.auth.service import UserService
from src.auth.dependencies import AccessTokenBearer,RefreshTokenBearer,get_current_user,RoleChecker
from src.auth.utils import verify_password,create_access_token
from src.auth.models import RefreshToken
from src.errors import InvalidCredentials, InvalidToken ,RevokedToken,UserAlreadyExists

user_service = UserService()
access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()
role_checker = RoleChecker(['admin'])


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
async def get_user_ById(uid: str,
                        session:AsyncSession=Depends(get_session),
                        admin:bool = Depends(role_checker)
                        ):
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
            expires_at = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRY)
            new_refresh_token = RefreshToken(
                user_id=user.uid,
                refresh_token=refresh_token,
                expires_at=expires_at
            )
            session.add(new_refresh_token)
            await session.commit()

            
            
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
    raise InvalidCredentials()


@auth_router.get('/refresh_token') 
async def get_new_access_token(token_details: dict = Depends(refresh_token_bearer),
                               session: AsyncSession = Depends(get_session)):

    expiry_timestamp = token_details['token_data']['exp']
    user_data = token_details['token_data']['user']
    token = token_details['token']

    #check expire
    if datetime.fromtimestamp(expiry_timestamp) <= datetime.now():
        raise InvalidToken()


    result = await session.exec(
        select(RefreshToken).where(RefreshToken.refresh_token == token)
    )
    db_token = result.first()

    if not db_token or db_token.is_revoked:
        raise RevokedToken()
    
    if db_token.expires_at <= datetime.now():
        raise InvalidToken()

    new_access_token = create_access_token(user_data=user_data)

    return JSONResponse(
        content={"access_token": new_access_token}
    )


@auth_router.get('/logout')
async def revook_token(token_details:dict = Depends(refresh_token_bearer),
                       session:AsyncSession = Depends(get_session)):

    token_str = token_details["token"]
    statement = select(RefreshToken).where(RefreshToken.refresh_token == token_str)
    result = await session.exec(statement)
    db_token = result.first()

    if not db_token or db_token.is_revoked:
        raise RevokedToken()
    
    db_token.is_revoked = True
    session.add(db_token)
    await session.commit()


    return JSONResponse(
        content= {
            "message": "logged out successfully",
            "status_code": status.HTTP_200_OK
                 }
                     )


@auth_router.get('/logoutAll')
async def revook_token(token_details:dict = Depends(refresh_token_bearer),
                       session:AsyncSession = Depends(get_session)):
    
    user_uid = token_details["user"]["user_uid"]

    tokens = await session.exec(
    select(RefreshToken).where(RefreshToken.user_id == user_uid)
            )
    for token in tokens:
        token.is_revoked = True
        session.add(token)
    await session.commit()

    
    
    
@auth_router.get('/me',response_model=UserAddressModel)
async def get_current_user(user = Depends(get_current_user)):
    return user

