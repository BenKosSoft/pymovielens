import numpy as np

_k_neighbours = 10
_sensitivity = 1
_epsilon = 0.1
_gamma = 0.1  # this can be calculated by formula

_new_movies = np.array([], np.float)


def pre_processing(movies):
    global _new_movies
    _low_freq_movies = np.array([], np.float)

    # truncate
    kth_similarity = movies[_k_neighbours - 1][1]
    threshold = kth_similarity - _gamma
    for (i, sim) in movies:
        if sim >= threshold:  # new movies
            element = np.array([i, sim], np.float)
            if len(_new_movies) == 0:
                _new_movies = np.append(_new_movies, element)
            else:
                _new_movies = np.vstack((_new_movies, element))
        else:  # low frequent movies
            if len(_low_freq_movies) == 0:
                _low_freq_movies = np.array([[i], threshold])
            else:
                _low_freq_movies[0].append(i)

    _new_movies = np.vstack((_new_movies, _low_freq_movies))

    # prepare data (format : [...[movie_id, similarity, exp_data, after_total_exp_data]...])
    exp_coefficient = _epsilon / (4*_k_neighbours)
    exp_data = np.array([], np.float)
    after_total_exp_data = np.array([], np.float)
    for movie in _new_movies:
        exp_data = np.append(exp_data, np.exp(movie[1]*exp_coefficient))
    _new_movies = np.concatenate((_new_movies, np.expand_dims(exp_data, axis=0).T), axis=1)
    for i, movie in enumerate(_new_movies):
        after_total_exp_data = np.append(after_total_exp_data, np.sum(_new_movies.T[2][i:]))
    _new_movies = np.concatenate((_new_movies, np.expand_dims(after_total_exp_data, axis=0).T), axis=1)
    print _new_movies


def sampling_bernoulli():
    pass


def sampling_weighted_selection():
    pass


def perturbation():
    pass


def get_exponential_recommendation_order(movies):
    pre_processing(movies)
    sampling_bernoulli()
    perturbation()
    pass
