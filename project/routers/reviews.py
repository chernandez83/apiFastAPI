from typing import List
from fastapi import HTTPException, APIRouter, Depends

from ..database import User, Movie, UserReview
from ..schemas import ReviewRequestModel, ReviewRequestPutModel, ReviewResponseModel

from ..common import get_current_user

router = APIRouter(prefix='/reviews', tags=['Reviews'])


@router.post('', response_model=ReviewResponseModel)
async def create_review(user_review: ReviewRequestModel, user: User = Depends(get_current_user)):

    if User.select().where(User.id == user.id).first() is None:
        raise HTTPException(status_code=404, detail='El usuario no existe')

    if Movie.select().where(Movie.id == user_review.movie_id).first() is None:
        raise HTTPException(status_code=404, detail='La película no existe')

    user_review = UserReview.create(
        user_id=user.id,
        movie_id=user_review.movie_id,
        review=user_review.review,
        score=user_review.score
    )

    return user_review


@router.get('', response_model=List[ReviewResponseModel])
async def get_reviews(page: int = 1, limit: int = 5):
    reviews = UserReview.select().paginate(page, limit)

    return [user_review for user_review in reviews]


@router.get('/{review_id}', response_model=ReviewResponseModel)
async def get_review(review_id: int):
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    if user_review is None:
        raise HTTPException(status_code=404, detail='La reseña no existe')

    return user_review


@router.put('/{review_id}', response_model=ReviewResponseModel)
async def update_review(review_id: int, review_request: ReviewRequestPutModel, user: User = Depends(get_current_user)):
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    
    if user_review is None:
        raise HTTPException(status_code=404, detail='La reseña no existe')
    
    if user_review.user_id != user.id:
        raise HTTPException(status_code=401, detail='El usuario no es propiertario de la reseña')

    user_review.review = review_request.review
    user_review.score = review_request.score
    user_review.save()

    return user_review


@router.delete('/{review_id}', response_model=ReviewResponseModel)
async def delete_review(review_id: int, user: User = Depends(get_current_user)):
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    if user_review is None:
        raise HTTPException(status_code=404, detail='La reseña no existe')
    
    if user_review.user_id != user.id:
        raise HTTPException(status_code=401, detail='El usuario no es propiertario de la reseña')

    user_review.delete_instance()

    return user_review
