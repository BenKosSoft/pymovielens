import utildb
import dictionary
import time
import neo4jdriver
import csv

record_time = False


# creates indexes for the labels
def create_index(label, label_id):
    if record_time:
        start = time.time()

    print("create_index start")
    with neo4jdriver.session.begin_transaction() as tx:
        tx.run(dictionary.index_query_create.format(label, label_id))
    print("create_index end")

    if record_time:
        end = time.time()
        print(end - start)


def create_movies():
    data = []
    if record_time:
        start = time.time()

    print("create_movies start")
    with open(dictionary.movie_csv, 'rb') as csv_file:
        iter_reader = iter(csv.reader(csv_file, delimiter=',', quotechar='"'))
        next(iter_reader)
        for row in iter_reader:
            data.append({"movie_id": int(row[0]), "title": row[1], "genres": row[2]})
            if len(data) == 10000:
                with neo4jdriver.session.begin_transaction() as tx:
                    tx.run(dictionary.movie_query_create, data=data)
                    tx.commit()
                    del data[:]
    with neo4jdriver.session.begin_transaction() as tx:
        tx.run(dictionary.movie_query_create, data=data)
        tx.commit()
        del data[:]
    print("create_movies end")

    if record_time:
        end = time.time()
        print(end - start)


def create_links():
    data = []
    if record_time:
        start = time.time()

    print("create_links start")
    with open(dictionary.link_csv, 'rb') as csv_file:
        iter_reader = iter(csv.reader(csv_file, delimiter=',', quotechar='"'))
        next(iter_reader)
        for row in iter_reader:
            data.append({"movie_id": int(row[0]), "imdbId": row[1], "tmdbId": row[2]})
            if len(data) == 10000:
                with neo4jdriver.session.begin_transaction() as tx:
                    tx.run(dictionary.link_query_create, data=data)
                    tx.commit()
                    del data[:]
    with neo4jdriver.session.begin_transaction() as tx:
        tx.run(dictionary.link_query_create, data=data)
        tx.commit()
        del data[:]
    print("create_links end")

    if record_time:
        end = time.time()
        print(end - start)


def create_ratings():
    data = []
    if record_time:
        start = time.time()

    print("create_ratings start")
    with open(dictionary.rating_csv, 'rb') as csv_file:
        iter_reader = iter(csv.reader(csv_file, delimiter=',', quotechar='"'))
        next(iter_reader)
        for row in iter_reader:
            data.append({"movie_id": int(row[1]), "user_id": int(row[0]), "rating": float(row[2]), "timestamp": row[3]})
            if len(data) == 10000:
                with neo4jdriver.session.begin_transaction() as tx:
                    tx.run(dictionary.rating_query_create, data=data)
                    tx.commit()
                    del data[:]
    with neo4jdriver.session.begin_transaction() as tx:
        tx.run(dictionary.rating_query_create, data=data)
        tx.commit()
        del data[:]
    print("create_ratings end")

    if record_time:
        end = time.time()
        print(end - start)


def create_tags():
    data = []
    if record_time:
        start = time.time()

    print("create_tags start")
    with open(dictionary.tag_csv, 'rb') as csv_file:
        iter_reader = iter(csv.reader(csv_file, delimiter=',', quotechar='"'))
        next(iter_reader)
        for row in iter_reader:
            data.append({"movie_id": int(row[1]), "user_id": int(row[0]), "tag": row[2], "timestamp": float(row[3])})
            if len(data) == 10000:
                with neo4jdriver.session.begin_transaction() as tx:
                    tx.run(dictionary.tag_query_create, data=data)
                    tx.commit()
                    del data[:]
    with neo4jdriver.session.begin_transaction() as tx:
        tx.run(dictionary.tag_query_create, data=data)
        tx.commit()
        del data[:]
    print("create_tags end")

    if record_time:
        end = time.time()
        print(end - start)


# get movie by id
def get_movie_by_id(movie_id):
    if record_time:
        start = time.time()

    print("return_movie start")
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(dictionary.movie_query_get_by_id, movie_id=movie_id)
        if utildb.is_record_empty(records):
            print "No record!"
        else:
            for record in records.records():
                title = record[0]["title"]
                print(title)
    print("return_movie end")

    if record_time:
        end = time.time()
        print(end - start)


# get average of ratings of specific movie
def get_avg_rating_of_movie(movie_id):
    if record_time:
        start = time.time()

    print("get_avg_rating_of_movie start")
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(dictionary.movie_query_get_avg_rating, movie_id=movie_id)
        if utildb.is_record_empty(records):
            print "No record!"
        else:
            for record in records:
                title = record["title"]
                avg = record["rating_avg"]
                print("%s has %s average rating" % (title, avg))
    print("get_avg_rating_of_movie end")

    if record_time:
        end = time.time()
        print(end - start)


# get average of ratings of users
def get_avg_rating_of_user(user_id):
    if record_time:
        start = time.time()

    print("get_avg_rating_of_user start")
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(dictionary.user_query_get_avg_rating, user_id=user_id)
        if utildb.is_record_empty(records):
            print "No record!"
        else:
            for record in records:
                user_id = record["user_id"]
                rating_avg = record["rating_avg"]
                print("%s has %s average rating" % (user_id, rating_avg))
    print("get_avg_rating_of_user end")

    if record_time:
        end = time.time()
        print(end - start)


#
def create_dynamic_similarity():
    pass


#
def create_static_similarity():
    pass


#
def get_all_movies():
    pass
