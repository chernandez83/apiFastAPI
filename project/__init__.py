from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .database import database as connection
from .database import User, Movie, UserReview

from .routers import user_router, review_router, movie_router

from .common import create_access_token

app = FastAPI(title='Proyecto para reseñas',
              description='En ese proyecto se utiliza para aprender FastAPI',
              version='1')

api_v1=APIRouter(prefix='/api/v1')

api_v1.include_router(user_router)
api_v1.include_router(review_router)
api_v1.include_router(movie_router)


@api_v1.post('/auth')
async def auth(data: OAuth2PasswordRequestForm = Depends()):
    user = User.authenticate(data.username, data.password)
    
    if user:
        return {
            'access_token': create_access_token(user),
            'token_type': 'Bearer'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credenciales inválidas',
            headers={'WWW-Authenthicate': 'Bearer'}
        )

app.include_router(api_v1)

@app.on_event('startup')
def startup():
    print('El servidor está iniciando.')
    if connection.is_closed():
        connection.connect()
        print('Conexión establecidad con la base de datos.')

    connection.create_tables([User, Movie, UserReview])


@app.on_event('shutdown')
def shutdown():
    print('El servidor está finalizando.')
    if not connection.is_closed():
        connection.close()
        print('Conexión finalizada con la base de datos.')


@app.get('/')
async def index():  # async para atender peticiones simultáneas
    return '¡Hola mundo!'


@app.get('/about')
async def about():
    '''A cerca del servidor'''
    return 'Servidor de entrenamiento'
