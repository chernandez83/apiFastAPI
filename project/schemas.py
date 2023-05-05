from pydantic import BaseModel, validator
from pydantic.utils import GetterDict

from peewee import ModelSelect

from typing import Any


class PeeweeGetterDict(GetterDict):
    
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)

        return res


class ResponseModel(BaseModel):
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class UserRequestModel(BaseModel):
    username: str
    password: str

    @validator('username')
    def username_validator(cls, username):
        if len(username) < 3 or len(username) > 50:
            raise ValueError('La longitud del nombre de usuario deber ser de entre 3 y 50 caracteres')

        return username


class UserReponseModel(ResponseModel):
    id: int
    username: str
    
    # class Config:
    #     orm_mode = True
    #     getter_dict = PeeweeGetterDict


class MovieRequestModel(BaseModel):
    title: str
    
    @validator('title')
    def title_validator(cls, title):
        if len(title) > 50:
            raise ValueError('La longitud del título no debe ser mayor a 50 caracteres')
        
        return title


class MovieResponseModel(ResponseModel):
    id: int
    title: str
    
    # class Config:
    #     orm_mode = True
    #     getter_dict = PeeweeGetterDict


# No hereda validaciones!
# class ReviewValidator():
    
#     @validator('score')
#     def score_validator(cls, score):
#         if score < 1 or score > 5:
#             raise ValueError('El score debe estar entre 1 y 5')
        
#         return score
    
#     @validator('review')
#     def review_validator(cls, review):
#         if len(review) < 3:
#             raise ValueError('La longitud de la reseña no es válida')
        
#         return review


class ReviewRequestModel(BaseModel):
    user_id: int
    movie_id: int
    review: str
    score: int
    
    @validator('score')
    def score_validator(cls, score):
        if score < 1 or score > 5:
            raise ValueError('El score debe estar entre 1 y 5')
        
        return score
    
    @validator('review')
    def review_validator(cls, review):
        if len(review) < 3:
            raise ValueError('La longitud de la reseña no es válida')
        
        return review


class ReviewResponseModel(ResponseModel):
    id: int
    #movie_id: int
    movie: MovieResponseModel
    review: str
    score: int
    
    # class Config:
    #     orm_mode = True
    #     getter_dict = PeeweeGetterDict


class ReviewRequestPutModel(BaseModel):
    review: str
    score: int
    
    @validator('score')
    def score_validator(cls, score):
        if score < 1 or score > 5:
            raise ValueError('El score debe estar entre 1 y 5')
        
        return score
    
    @validator('review')
    def review_validator(cls, review):
        if len(review) < 3:
            raise ValueError('La longitud de la reseña no es válida')
        
        return review