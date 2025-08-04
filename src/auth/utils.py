from passlib.context import CryptContext
from datetime import timedelta,datetime
import jwt
import uuid
from src.config import config
import logging
from itsdangerous import URLSafeTimedSerializer

ACCESS_TOKEN_EXPIRY = 3600

password_context = CryptContext(
    schemes=['bcrypt']
)


def generate_password_hash(password:str) ->str:
    hash = password_context.hash(password)
    return hash

def verify_password(password:str , hash:str) -> bool:
    return password_context.verify(password,hash)


def create_access_token(user_data:dict,
                        expiry:timedelta=None,
                        refresh:bool=False):

    payload={}
    payload['user'] = user_data
    payload['exp'] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh

    token = jwt.encode(
        payload=payload,
        key= config.JWT_SECRETS,
        algorithm= config.JWT_ALGORITHM
    )

    return token

def decode_token(token:str) -> dict:

    try:
        token_data = jwt.decode(
            jwt=token,
            key=config.JWT_SECRETS,
            algorithms=[config.JWT_ALGORITHM]
        )

        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None

serializer = URLSafeTimedSerializer(
    secret_key=config.JWT_SECRETS,
    salt= "email.configuration"
)


def create_url_safe_token(data:dict):
   
    token = serializer.dumps(data,salt= "email.configuration")
    return token


def decode_url_safe_token(token:str):
    try:
        token_data = serializer.loads(token)
        return token_data
    
    except Exception as e:
        logging.error(e)
