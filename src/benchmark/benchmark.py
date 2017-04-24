from src import db
import csv
import time

base_dir = "../../res_unshared/"
subfolder = "ml-mini/"

_TEST_RATIO = 0.2


def predict(user_id, movie_id):
    sims = db.get_similarities_by_movie(movie_id)
    ratings = db.get_ratings_of_user(user_id)

    weighted_sum, count = 0, 0
    for key in ratings:
        if key in sims:
            weighted_sum += sims[key] * ratings[key]
            count += sims[key]
    return weighted_sum / count if count != 0 else None


def avg_error():
    error_sum, count = 0, 0
    with open(base_dir + subfolder + "ratings_test_{}.csv".format(_TEST_RATIO)) as r_test:
        csvr = csv.DictReader(r_test, delimiter=',', quotechar='"')
        for row in csvr:
            prediction = predict(int(row["userId"]), int(row["movieId"]))
            if prediction:
                count += 1
                error_sum += abs(prediction - float(row["rating"]))
    return error_sum / count if count > 0 else None


if __name__ == '__main__':
    start = time.time()
    error = avg_error()
    end = time.time()
    print 'Mean Average Error is', error
    print "Execution time: ", end-start
