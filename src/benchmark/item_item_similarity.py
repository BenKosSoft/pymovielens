from src import db
from src import paths
import csv
import time

_TEST_RATIO = 0.2
_k_neighbours = 5


def predict(user_id, movie_id):
    return db.get_prediction_by_user_and_movie_id(user_id, movie_id, _k_neighbours)


def avg_error():
    error_sum, count = 0, 0
    with open(paths.ratings_mini_test_csv.format(_TEST_RATIO)) as r_test:
        csvr = csv.DictReader(r_test, delimiter=',', quotechar='"')
        for row in csvr:
            prediction = predict(int(row["userId"]), int(row["movieId"]))
            if prediction != -1:
                count += 1
                error_sum += abs(prediction - float(row["rating"]))
    return error_sum / count if count > 0 else None


if __name__ == '__main__':
    start = time.time()
    error = avg_error()
    end = time.time()
    print 'Mean Average Error is', error
    print "Execution time: ", end - start
