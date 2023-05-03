from fastapi import FastAPI

from database import database as connection
from database import User, Movie, UserReview

from schemas import UserBaseModel

app = FastAPI(title='Proyecto para reseñas',
              description='En ese proyecto se utiliza para aprender FastAPI',
              version='1')


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


@app.post('/users/')
async def create_user(user: UserBaseModel):
    user = User.create(
        username=user.username,
        password=user.password
    )
    
    return user.id