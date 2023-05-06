from fastapi import HTTPException, APIRouter
from typing import List

from ..database import Movie
from ..schemas import MovieRequestModel, MovieResponseModel
from ..schemas import ReviewResponseModel

router = APIRouter(prefix='/movies')


@router.get('', response_model=List[MovieResponseModel])
async def get_movies(page: int = 1, limit: int = 5):
    movies = Movie.select().paginate(page, limit)

    return [movie for movie in movies]


@router.post('', response_model=MovieResponseModel)
async def create_movie(movie: MovieRequestModel):
    if Movie.select().where(Movie.title == movie.title).exists():
        raise HTTPException(409, 'La película ya existe')

    movie = Movie.create(
        title=movie.title
    )

    return movie


@router.get('/reviews/{movie_id}', response_model=List[ReviewResponseModel])
async def get_reviews(movie_id: int):
    movie = Movie.select().where(Movie.id == movie_id).first()
    
    if movie is None:
        raise HTTPException(status_code=404, detail='La película no existe')
    
    print(movie)
    return [user_review for user_review in movie.reviews]