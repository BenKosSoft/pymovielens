from src import db
from src import utility as util

k_neighbours = 5
movie_ids = [1]


def main():
    for movie_id in movie_ids:
        movies = db.get_similarities_by_movie(movie_id, k_neighbours)
        new_order = util.get_exponential_recommendation_order(movies)
        print movies, new_order


if __name__ == '__main__':
    main()
