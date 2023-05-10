import jwt
from datetime import datetime, timedelta
from decouple import config
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .database import User

SECRET_KEY = config('SECRET_KEY')

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/api/v1/auth')


def create_access_token(user, days=7):
    data = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(days=days)
    }

    return jwt.encode(data, key=SECRET_KEY, algorithm='HS256')


def decode_access_token(token: str = Depends(oauth2_schema)):
    try:
        return jwt.decode(token, key=SECRET_KEY, algorithms=['HS256'])
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Access token expiró',
            headers={'WWW-Authenthicate': 'Bearer'}
        )


def get_current_user(token: str = Depends(oauth2_schema))  -> User:
    data = decode_access_token(token)
    
    print(data)
    
    return User.select().where(User.id == data['user_id']).first()