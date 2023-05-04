from fastapi import FastAPI, HTTPException

from database import database as connection
from database import User, Movie, UserReview

from schemas import UserRequestModel, UserReponseModel

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


@app.post('/users', response_model=UserReponseModel)
async def create_user(user: UserRequestModel):
    if User.select().where(User.username == user.username).exists():
        raise HTTPException(409, 'El nombre de usuario ya se encuentra en uso')
    
    hash_passord = User.create_password(user.password)
    user = User.create(
        username=user.username,
        password=hash_passord
    )
    
    # return {
    #     'id': user.id,
    #     'username': user.username,
    # }
    return UserReponseModel(id=user.id, username=user.username)