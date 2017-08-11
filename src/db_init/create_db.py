import time
import sys

from src.strings import paths
from src.utility import db
from src.utility.logger import Logger

# logger
__log = Logger()

# time recording
__record_time = True


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
    if __record_time:
        start = time.time()

    create_database()

    if __record_time:
        end = time.time()
        __log.info('CREATE_DB takes %f seconds' % (end-start))
        sys.stdout.write('\nCREATE_DB takes %f seconds\n\n' % (end-start))
