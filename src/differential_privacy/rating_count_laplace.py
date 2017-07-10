import numpy as np
from src import db

# differentially private count query
_sensitivity = 1
_epsilon = 0.1
_scale = _sensitivity / _epsilon
_rand = np.random


# dif private count movie rating by movie id
def get_private_count(movie_id):
    movie_rating_count = db.get_movie_rating_count(movie_id)
    noisy_count = _rand.laplace(scale=_scale) + movie_rating_count
    return movie_rating_count, noisy_count
