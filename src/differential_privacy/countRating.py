import numpy as np
from src import db

# differentially private count query
mu = 0
sensitivity = 1
epsilon = 0.1
scale = sensitivity / epsilon
precision = 0.001
rand = np.random

# create some randomly distributed data:
# noise = rand.laplace(0, scale, 10000)
# print np.max(noise), np.min(noise), np.mean(noise), np.std(noise)


# dif private count movie rating by movie id
def get_private_count(movie_id):
    movie_rating_count = db.get_movie_rating_count(movie_id)
    noisy_count = rand.laplace(scale=scale) + movie_rating_count
    return movie_rating_count, noisy_count


def main():
    movies = [1, 10, 32, 34, 47]
    for movie in movies:
        movie_rating_count, noisy_count = get_private_count(movie)
        print movie, movie_rating_count, noisy_count


if __name__ == '__main__':
    main()
