from typing import List
from fastapi import HTTPException, APIRouter, Response, Depends, Cookie, Header
from fastapi.security import HTTPBasicCredentials

from ..database import User
from ..schemas import UserRequestModel, UserReponseModel
from ..schemas import ReviewResponseModel

from ..common import oauth2_schema, get_current_user

router = APIRouter(prefix='/users', tags=['Authentication'])


@router.post('', response_model=UserReponseModel)
async def create_user(user: UserRequestModel):
    if User.select().where(User.username == user.username).exists():
        raise HTTPException(409, 'El nombre de usuario ya se encuentra en uso')

    hash_passord = User.create_password(user.password)
    user = User.create(
        username=user.username,
        password=hash_passord
    )

    return user


@router.post('/login', response_model=UserReponseModel)
async def login(credentials: HTTPBasicCredentials, response: Response):
    user = User.select().where(User.username == credentials.username).first()
    
    if user is None:
        raise HTTPException(status_code=404, detail='Usuario no existe.')
    
    if user.password != User.create_password(credentials.password):
        raise HTTPException(status_code=409, detail='Contraseña incorrecta.')
    
    response.set_cookie(key='user', value=user.username)
    response.set_cookie(key='user_id', value=user.id)
    return user


# @router.get('/reviews', response_model=List[ReviewResponseModel])
# async def get_reviews(user_id: int = Cookie(None)):
#     user = User.select().where(User.id == user_id).first()
    
#     if user is None:
#         raise HTTPException(status_code=404, detail='Usuario no existe.')
    
#     return [user_review for user_review in user.reviews]

# @router.get('/reviews') #, response_model=List[ReviewResponseModel])
# async def get_reviews(token: str = Depends(oauth2_schema)):
#     return {
#         'token': token
#     }
    
    
@router.get('/reviews', response_model=List[ReviewResponseModel])
async def get_reviews(user: User = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=404, detail='Usuario no existe.')
    
    return [user_review for user_review in user.reviews]