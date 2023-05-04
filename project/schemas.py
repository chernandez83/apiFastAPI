from pydantic import BaseModel, validator
from pydantic.utils import GetterDict


class PeeweeGetterDict(GetterDict):
    pass


class UserRequestModel(BaseModel):
    username: str
    password: str

    @validator('username')
    def username_validator(cls, username):
        if len(username) < 3 or len(username) > 50:
            raise ValueError(
                'La longitud del nombre de usuario deber ser de entre 3 y 50 caracteres')

        return username


class UserReponseModel(BaseModel):
    id: int
    username: str
