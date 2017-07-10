# TODO: Movieleri databaseden al
# TODO: Similarity query'sini kontrol et, (asagidaki fonksyionlari)

from src import db
from src.differential_privacy import exponential_mechanism as em

movie_ids = [1]


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
    for movie_id in movie_ids:
        movies = db.get_similarities_by_movie(movie_id)
        new_order = em.get_exponential_recommendation_order(movies)

        # change movies array with ids in array
        movies = [m[0] for m in movies]
        print movies, new_order

        error += benchmark(movies, new_order.tolist())

    print "Error is ", error


if __name__ == '__main__':
    main()
