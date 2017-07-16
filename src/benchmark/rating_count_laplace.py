from src.differential_privacy import rating_count_laplace as rcl


# TODO: add benchmark, take movies from database
def main():
    movies = [1, 10, 32, 34, 47]
    for movie in movies:
        movie_rating_count, noisy_count = rcl.get_private_count(movie)
        print movie, movie_rating_count, noisy_count


if __name__ == '__main__':
    main()
