from src import db
from src import paths
import time

_record_time = False


def create_indexes():
    db.create_index("Movie", "movie_id")
    db.create_index("User", "user_id")


def create_movies():
    db.create_movies(paths.movies_mini_csv)


def create_ratings():
    db.create_ratings(paths.ratings_mini_csv)


def create_links():
    pass


def create_tags():
    pass


def create_database():
    create_indexes()
    create_movies()
    create_ratings()
    create_links()
    create_tags()


if __name__ == '__main__':
    if _record_time:
        start = time.time()

    create_database()

    if _record_time:
        end = time.time()
        print(end - start)
