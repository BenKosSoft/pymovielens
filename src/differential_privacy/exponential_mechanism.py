import numpy as np


class ExponentialMechanism:
    """
    Exponential mechanism for differentially private applications
    """

    # ==================================================================================================================
    # Private
    # ==================================================================================================================
    def __init__(self, k_neighbours=10, sensitivity=1, epsilon=0.1, gamma=0.1):
        """
        Initialize privatization parameters to apply exponential mechanism functionalities
        :param k_neighbours: Nearest neighbour count
        :param sensitivity:  Sensitivity coefficient
        :param epsilon:      Epsilon value for, epsilon-differentially private queries
        :param gamma:        Accepted error range below or above calculated similarity value
        """
        self.__k_neighbours = k_neighbours
        self.__sensitivity = sensitivity
        self.__epsilon = epsilon
        self.__gamma = gamma  # todo: calculate gamma value with formula
        self.__new_movies = np.array([], np.float)

    def __pre_processing(self, movies):
        _low_freq_movies = np.array([], np.float)

        # truncate
        kth_similarity = movies[self.__k_neighbours - 1][1]
        threshold = kth_similarity - self.__gamma
        for (i, sim) in movies:
            if sim >= threshold:  # new movies
                element = np.array([i, sim], np.float)
                if len(self.__new_movies) == 0:
                    self.__new_movies = np.append(self.__new_movies, element)
                else:
                    self.__new_movies = np.vstack((self.__new_movies, element))
            else:  # low frequent movies
                if len(_low_freq_movies) == 0:
                    _low_freq_movies = np.array([[i], threshold])
                else:
                    _low_freq_movies[0].append(i)

        self.__new_movies = np.vstack((self.__new_movies, _low_freq_movies))

        # prepare data (format : [...[movie_id, similarity, exp_data, after_total_exp_data]...])
        exp_coefficient = self.__epsilon / (4 * self.__k_neighbours)
        exp_data = np.array([], np.float)
        after_total_exp_data = np.array([], np.float)
        for movie in self.__new_movies:
            exp_data = np.append(exp_data, np.exp(movie[1] * exp_coefficient))
        self.__new_movies = np.concatenate((self.__new_movies, np.expand_dims(exp_data, axis=0).T), axis=1)
        for i, movie in enumerate(self.__new_movies):
            after_total_exp_data = np.append(after_total_exp_data, np.sum(self.__new_movies.T[2][i:]))
        self.__new_movies = np.concatenate((self.__new_movies, np.expand_dims(after_total_exp_data, axis=0).T), axis=1)
        print self.__new_movies  # todo: use Logger Class

    def __sampling_bernoulli(self, movies):
        pass

    def __sampling_weighted_random(self, movies):
        pass

    def __perturbation(self, movies):
        pass

    # ==================================================================================================================
    # Public
    # ==================================================================================================================
    def get_exponential_recommendation_order(self, movies):
        self.__pre_processing(movies)
        self.__sampling_bernoulli(movies)
        self.__perturbation(movies)
