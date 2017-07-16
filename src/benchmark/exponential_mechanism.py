# TODO: Movieleri databaseden al
# TODO: Similarity query'sini kontrol et, (asagidaki fonksyionlari)

from src.differential_privacy.exponential_mechanism import *
from src.utility import db

movie_ids = [5952]


# expected: expected array with sequence of movie ids
# result: result array after differential privacy with sequence of movie ids
# return: mean error of order of movie ids
def benchmark(expected, result):
    error = 0
    for i, el in enumerate(expected):
        error += abs(i - result.index(el))
    return error / float(len(expected))


def main():
    error = 0
    em = ExponentialMechanism()
    for movie_id in movie_ids:
        movies = db.get_similarities_by_movie(movie_id)
        new_order = em.get_exponential_recommendation_order(movies)

        # change movies array with ids in array
        movies = [m[0] for m in movies]
        print movies, new_order  # todo: use Logger Class

        error += benchmark(movies, new_order.tolist())

    print "Error is ", error  # todo: use Logger Class


if __name__ == '__main__':
    main()
