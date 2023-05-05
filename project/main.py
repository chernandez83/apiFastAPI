from fastapi import FastAPI, HTTPException
from typing import List

from database import database as connection
from database import User, Movie, UserReview

from schemas import UserRequestModel, UserReponseModel
from schemas import ReviewRequestModel, ReviewResponseModel, ReviewRequestPutModel
from schemas import MovieRequestModel, MovieResponseModel

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
    # return UserReponseModel(id=user.id, username=user.username)
    return user


@app.post('/movies', response_model=MovieResponseModel)
async def create_movie(movie: MovieRequestModel):
    if Movie.select().where(Movie.title == movie.title).exists():
        raise HTTPException(409, 'La película ya existe')

    movie = Movie.create(
        title=movie.title
    )

    return movie


@app.post('/reviews', response_model=ReviewResponseModel)
async def create_review(user_review: ReviewRequestModel):

    if User.select().where(User.id == user_review.user_id).first() is None:
        raise HTTPException(status_code=404, detail='El usuario no existe')

    if Movie.select().where(Movie.id == user_review.movie_id).first() is None:
        raise HTTPException(status_code=404, detail='La película no existe')

    user_review = UserReview.create(
        user_id=user_review.user_id,
        movie_id=user_review.movie_id,
        review=user_review.review,
        score=user_review.score
    )

    return user_review


@app.get('/reviews', response_model=List[ReviewResponseModel])
async def get_reviews(page: int = 1, limit: int = 5):
    reviews = UserReview.select().paginate(page, limit)

    return [user_review for user_review in reviews]


@app.get('/reviews/{review_id}', response_model=ReviewResponseModel)
async def get_review(review_id: int):
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    if user_review is None:
        raise HTTPException(status_code=404, detail='La reseña no existe')

    return user_review


@app.put('/reviews/{review_id}', response_model=ReviewResponseModel)
async def update_review(review_id: int, review_request: ReviewRequestPutModel):
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    if user_review is None:
        raise HTTPException(status_code=404, detail='La reseña no existe')

    user_review.review = review_request.review
    user_review.score = review_request.score
    user_review.save()

    return user_review


@app.delete('/reviews/{review_id}', response_model=ReviewResponseModel)
async def delete_review(review_id: int):
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    if user_review is None:
        raise HTTPException(status_code=404, detail='La reseña no existe')

    user_review.delete_instance()

    return user_review
