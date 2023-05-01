from pydantic import BaseModel, validator, ValidationError
from typing import Optional

class User(BaseModel):
    username: str
    password: str
    repeat_password: str
    email: str
    edad: Optional[int] = None
    
    @validator('username')
    def username_validation_length(cls, username):
        if len(username) < 3:
            raise ValueError('La longitud del nombre de usuario es de mínimo 3 caracteres')
        if len(username) > 50:
            raise ValueError('La longitud del nombre de usuario es de máximo 50 caracteres')
        return username
    
    @validator('repeat_password')
    def repeat_password_validation(cls, repeat_password, values):
        if 'password' in values and repeat_password != values['password']:
            raise ValueError('Las contraseñas no coinciden')
        return repeat_password


try:
    batman = User(
        username='Batman',
        password='Robin',
        repeat_password='Roba',
        email='batman@jl.com',
        # edad=32
    )
    print(batman)
except ValidationError as e:
    print(e.json())