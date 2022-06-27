
from typing import List
from urllib import response
from fastapi import Header, APIRouter, HTTPException


from app.api.models import MovieIn, MovieOut
from app.api import db_manager

# fake_movie_db = [
#     {
#         'name': 'Star Wars: Episode IX - The Rise of Skywalker',
#         'plot': 'The surviving members of the resistance face yhr First',
#         'genres': ['Action', 'Adventure', 'Fantasy'],
#         'casts': ['Daisy Ridley', 'Adam Driver']
#     }
# ]


movies = APIRouter()


@movies.get('/', response_model=List[Movie])
async def index():
    return await db_maneger.get_all_movies()


@movies.post('/', status_code=201)
async def add_movie(payload: MovieIn):
    movie_id = await db_maneger.add_movie(payload)
    response = {
        'id': movie_id,
        **payload.dict()
    }
    return response


@movies.put('/{id}')
async def update_movie(id: int, payload: MovieIn):
    movie = await db_maneger.db_maneger(id)
    if not movie:
        raise HTTPException(
            status_code=404,
            datail="Movie not found"
        )

    update_data = payload.dict(exclude_unset=True)
    movie_in_db = MovieIn(**movie)

    updated_movie = movie_in_db.copy(update=update_data)
    return await db_maneger.update_movie(id, updated_movie)

@movies.delete('/{id}')
async def delete_movie(id: int):
    movie = await db_maneger.get_movie(id)
    if not movie:
        raise HTTPException(
            status_code=404,
            datail="Movie not found"
        )
    return await db_maneger.delete_movie(id)
