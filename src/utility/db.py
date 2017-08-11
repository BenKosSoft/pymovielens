import csv

from src.strings import queries
from src.utility import neo4jdriver, file
from src.utility.logger import Logger
from src.utility.progressBar import ProgressBar

# logger
__log = Logger()


# todo: utilize progressBar in this file

# creates indexes for the labels
def create_index(label, label_id):
    __log.info("create_index start for " + label + ":" + label_id)
    with neo4jdriver.session.begin_transaction() as tx:
            tx.run(queries.index_query_create.format(label, label_id))


def create_movies(path):
    movie_count = file.count_row_csv(path)
    pb = ProgressBar(movie_count, 'Movie Creation', 'Complete')
    batch = 10000

    __log.info("create_movies start")
    data = []
    with open(path, 'rb') as movies:
        csvr = csv.DictReader(movies, delimiter=',', quotechar='"')
        for row in csvr:
            data.append({"movie_id": int(row['movieId']), "title": row['title'], "genres": row['genres']})
            if len(data) == batch:
                with neo4jdriver.session.begin_transaction() as tx:
                    tx.run(queries.movie_query_create, data=data)
                    tx.commit()
                pb.print_progress(batch)
                del data[:]
    with neo4jdriver.session.begin_transaction() as tx:
        tx.run(queries.movie_query_create, data=data)
        tx.commit()
    pb.print_progress(len(data))
    del data[:]


def create_links(path):
    __log.info("create_links start")
    data = []
    with open(path, 'rb') as csv_file:
        iter_reader = iter(csv.reader(csv_file, delimiter=',', quotechar='"'))
        next(iter_reader)
        for row in iter_reader:
            data.append({"movie_id": int(row[0]), "imdbId": row[1], "tmdbId": row[2]})
            if len(data) == 10000:
                with neo4jdriver.session.begin_transaction() as tx:
                    tx.run(queries.link_query_create, data=data)
                    tx.commit()
                    del data[:]
    with neo4jdriver.session.begin_transaction() as tx:
        tx.run(queries.link_query_create, data=data)
        tx.commit()
        del data[:]


def create_ratings(path):
    __log.info("create_ratings start")
    rating_count = file.count_row_csv(path)
    pb = ProgressBar(rating_count, 'Rating Creation', 'Complete')
    batch = 10000

    data = []
    with open(path, 'rb') as ratings:
        csvr = csv.DictReader(ratings, delimiter=',', quotechar='"')
        for row in csvr:
            data.append({"movie_id": int(row['movieId']),
                         "user_id": int(row['userId']),
                         "rating": float(row['rating']),
                         "timestamp": row['timestamp']})
            if len(data) == batch:
                with neo4jdriver.session.begin_transaction() as tx:
                    tx.run(queries.rating_query_create, data=data)
                    tx.commit()
                pb.print_progress(batch)
                del data[:]
    with neo4jdriver.session.begin_transaction() as tx:
        tx.run(queries.rating_query_create, data=data)
        tx.commit()
    pb.print_progress(len(data))
    del data[:]


def create_tags(path):
    __log.info("create_tags start")
    data = []
    with open(path, 'rb') as csv_file:
        iter_reader = iter(csv.reader(csv_file, delimiter=',', quotechar='"'))
        next(iter_reader)
        for row in iter_reader:
            data.append({"movie_id": int(row[1]), "user_id": int(row[0]), "tag": row[2], "timestamp": float(row[3])})
            if len(data) == 10000:
                with neo4jdriver.session.begin_transaction() as tx:
                    tx.run(queries.tag_query_create, data=data)
                    tx.commit()
                    del data[:]
    with neo4jdriver.session.begin_transaction() as tx:
        tx.run(queries.tag_query_create, data=data)
        tx.commit()
        del data[:]


# get movie by id
def get_movie_by_id(movie_id):
    __log.info("return_movie start")
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(queries.movie_query_get_by_id, movie_id=movie_id)
        data = records.data()
        if len(data) == 0:
            __log.warning("No record in get_movie_by_id: " + movie_id)
        else:
            row = data[0]
            title = row["title"]
            genres = row['genres']
            return title, genres


# get average of ratings of specific movie
def get_avg_rating_of_movie(movie_id):
    __log.info("get_avg_rating_of_movie start")
    with neo4jdriver.session.begin_transaction() as tx:
        data = tx.run(queries.movie_query_get_avg_rating, movie_id=movie_id).data()
        if len(data) == 0:
            __log.warning("No record in get_avg_rating_of_movie: " + movie_id)
        else:
            row = data[0]
            title = row["title"]
            avg = row["rating_avg"]
            return title, avg


# get average of ratings of users
def get_avg_rating_of_user(user_id):
    __log.info("get_avg_rating_of_user start: " + user_id)
    with neo4jdriver.session.begin_transaction() as tx:
        data = tx.run(queries.user_query_get_avg_rating, user_id=user_id).data()
        if len(data) == 0:
            __log.warning("No record in get_avg_rating_of_user: " + user_id)
        else:
            row = data[0]
            rating_mean = row["rating_avg"]
            return rating_mean


# get average of ratings of all users
def get_avg_rating_of_all_user():
    __log.info("get_avg_rating_of_user start")
    users_rating_avg = {}
    with neo4jdriver.session.begin_transaction() as tx:
        data = tx.run(queries.user_query_get_all_avg_rating).data()
        if len(data) == 0:
            __log.warning("No record in get_avg_rating_of_user")
        else:
            for row in data:
                user_id = row["user_id"]
                rating_mean = row["rating_avg"]
                users_rating_avg[user_id] = rating_mean
    return users_rating_avg


#
def create_dynamic_similarity(data):
    __log.info("create_dynamic_similarity start")
    with neo4jdriver.session.begin_transaction() as tx:
        tx.run(queries.movie_query_create_dynamic_similarity, data=data)
        tx.commit()
    __log.info("create_dynamic_similarity end")


#
def create_static_similarity():
    pass


#
def get_all_movies():
    pass


#
def get_by_ratings_movie_ids(movie1_id, movie2_id):
    __log.info("get_by_ratings_movie_ids start: %f, %f" % (movie1_id, movie2_id))
    with neo4jdriver.session.begin_transaction() as tx:
        data = tx.run(queries.movie_movie_query_adjusted_cosine,
                      movie1_id=movie1_id, movie2_id=movie2_id).data()
    return data


# get count of movie
def get_movie_ids():
    __log.info("get_movie_count start")
    result = []
    with neo4jdriver.session.begin_transaction() as tx:
        data = tx.run(queries.movie_query_get_all_movie_ids).data()
        for row in data:
            result.append(row["movie_id"])
    return result


# returns list of (otherMovieId, similarity) of movie
def get_prediction_by_user_and_movie_id(user_id, movie_id, k_neighbours=5):
    __log.info("get_prediction_by_user_and_movie_id start: {}-{}-{}"
               .format(user_id, movie_id, k_neighbours))
    prediction = -1
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(queries.user_movie_query_get_prediction,
                         movie_id=movie_id, user_id=user_id, k_neighbours=k_neighbours)
        for record in records:
            prediction = record["prediction"]
    return prediction


# get movie rating count by movie id
def get_movie_rating_count(movie_id):
    count = -1
    with neo4jdriver.session.begin_transaction() as tx:
        data = tx.run(queries.movie_rating_count_query_by_id, movie_id=movie_id).data()
        if len(data) == 0:
            __log.warning("No record in get_movie_rating_count: " + movie_id)
        else:
            row = data[0]
            count = row['count']
    return count


# get similarities of k-nearest movie by movie id
def get_similarities_by_movie_k_n(movie_id, k_neighbours):
    result = []
    with neo4jdriver.session.begin_transaction() as tx:
        data = tx.run(queries.similarities_by_movie_neighbour,
                      movie_id=movie_id, k_neighbours=k_neighbours).data()
        if len(data) <= 0:
            __log.warning("No record in get_similarities_by_movie_k_n: {}-{}"
                          .format(movie_id, k_neighbours))
        else:
            for row in data:
                movie2_id = row['movie2_id']
                sim = row['sim']
                result.append((movie2_id, sim))
    return result


# get similarities by movie id
def get_similarities_by_movie(movie_id):
    result = []
    with neo4jdriver.session.begin_transaction() as tx:
        data = tx.run(queries.similarities_by_movie,
                      movie_id=movie_id).data()
        if len(data) == 0:
            __log.warning("No record in get_similarities_by_movie: {}"
                          .format(movie_id))
        else:
            for row in data:
                movie2_id = row['movie2_id']
                sim = row['sim']
                result.append((movie2_id, sim))
    return result
