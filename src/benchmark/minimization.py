import csv
import os
import operator

base_dir = "../../res_unshared/"
movie_csv = "../../res_unshared/ml-latest-small/movies.csv"
rating_csv = "../../res_unshared/ml-latest-small/ratings.csv"

_movie_count = 10


def most_rated_movies():
    movie_dict = {}
    with open(rating_csv) as ratings:
        csvr = csv.DictReader(ratings, delimiter=',', quotechar='"')
        for row in csvr:
            index = row["movieId"]
            value = movie_dict.get(index, None)
            if not value:
                movie_dict[index] = 1
            else:
                movie_dict[index] += 1

    sorted_movie = sorted(movie_dict.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_movie[0:_movie_count]


def create_new_csv(new_path, movie_dict, old_csv):
    if os.path.exists(os.path.dirname(new_path)) and os.path.isdir(os.path.dirname(new_path)):
        pass
    else:
        os.makedirs(os.path.dirname(new_path))

    with open(new_path, 'wb') as new_csv:
        with open(old_csv) as data:
            csvr = csv.DictReader(data, delimiter=',', quotechar='"')
            csvw = csv.DictWriter(new_csv, fieldnames=csvr.fieldnames)
            csvw.writeheader()
            for row in csvr:
                index = row["movieId"]
                value = movie_dict.get(index, None)
                if not value:
                    pass
                else:
                    csvw.writerow(row)


def main():
    new_movies_path = base_dir + "ml-mini-small/movies.csv"
    new_ratings_path = base_dir + "ml-mini-small/ratings.csv"
    movie_dict = dict(most_rated_movies())

    create_new_csv(new_movies_path, movie_dict, movie_csv)
    create_new_csv(new_ratings_path, movie_dict, rating_csv)

if __name__ == '__main__':
    main()
