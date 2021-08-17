import os
from datetime import timedelta, datetime
from dotenv import load_dotenv
from jose import JWTError, jwt
from schemas import schemas

load_dotenv()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv(
        'SECRET_KEY'), algorithm=os.getenv('ALGORITHM'))
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'),
                             algorithms=[os.getenv('ALGORITHM')])
        email: str = payload.get("sub")
        if not email:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
