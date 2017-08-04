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
        :type k_neighbours:  int
        :param sensitivity:  Sensitivity coefficient
        :type sensitivity:   float
        :param epsilon:      Epsilon value for, epsilon-differentially private queries
        :type epsilon:       float
        :param gamma:        Accepted error range below or above calculated similarity value
        :type gamma:         float
        """
        self.__k_neighbours = k_neighbours
        self.__sensitivity = sensitivity
        self.__epsilon = epsilon
        self.__gamma = gamma  # todo: calculate gamma value with formula
        self.__new_movies = None

    def __pre_processing(self, movies):
        """
        Pre-processing step: differentiate values above and below threshold, which to be used in sampling step. Also
        prepares the array which the sampling will take place
        :param movies: array of movies in which the pre-processing step will take place. Length of movies should be at
                    least equal to self.__k_neighbours, otherwise error will occur
        """
        self.__new_movies = np.array([], np.float)
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
        # todo: replace arbitrary scaling factor (10000) with a calculated value
        exp_coefficient = self.__epsilon * 10000 / (4 * self.__k_neighbours * self.__sensitivity)
        exp_data = np.array([], np.float)
        after_total_exp_data = np.array([], np.float)
        for movie in self.__new_movies:
            exp_data = np.append(exp_data, np.exp(movie[1] * exp_coefficient))
        self.__new_movies = np.concatenate((self.__new_movies, np.expand_dims(exp_data, axis=0).T), axis=1)
        for i, movie in enumerate(self.__new_movies):
            after_total_exp_data = np.append(after_total_exp_data, np.sum(self.__new_movies.T[2][i:]))
        self.__new_movies = np.concatenate((self.__new_movies, np.expand_dims(after_total_exp_data, axis=0).T), axis=1)

        # todo: add structure to the array for easier usability
        # todo: sort the result with respect to expData (very easy if we can manage the above todo)

        print self.__new_movies  # todo: use Logger Class

    def __update_total_exp(self, index):
        """
        Iterates over self.__new_movies array to update after_total_exp_data of all of the elements up to the given
        index value, using the exp_data value of the element at given index.
        :param index: index of the element, which will be used to update the array
        """
        if index >= len(self.__new_movies) or -index >= len(self.__new_movies):
            msg = 'Index out of bounds'
            print msg, ' index: ', index, ' array length: ', len(self.__new_movies)  # todo: use Logger class
            raise IndexError(msg)

        for i in range(len(self.__new_movies)):
            if i < index:
                self.__new_movies[i][3] -= self.__new_movies[index][2]  # todo: update indices with names

    def __sampling_bernoulli(self):
        """
        Sampling step using Bernoulli: Sample each movie's probability of being chosen from Bernoulli distribution
        individually. As a result construct a new array which will contain a differentially private order of movies
        according to their similarities.
        :return: Array of movies of length self.__k_neighbours, which differentially privately ordered by their
        similarity values
        """
        if len(self.__new_movies) == 0:
            return

        output, chosen_low_freq = None, None

        for i in range(self.__k_neighbours):
            is_picked = False
            j = 0
            while not is_picked:
                # take random boolean result using calculated probabilities
                # todo: update indices with name
                is_chosen = np.random.binomial(1, self.__new_movies[j][2] / self.__new_movies[j][3])

                if j == len(self.__new_movies) - 1:
                    is_picked = True

                    # chose from unchosen low frequency items
                    # todo: update indices with names
                    choice = np.random.choice(self.__new_movies[-1][0], 1)
                    output_item = np.array([(choice[0], self.__new_movies[-1][1])],
                                           dtype=[('movie_id', np.int32), ('similarity', np.float32)])

                    if output is None:
                        output = np.array(output_item)
                    else:
                        output = np.append(output, output_item)

                    # remove selected movie from low frequency items, to prevent it getting selected again
                    for k, movie in enumerate(self.__new_movies[-1]):
                        if movie[0] == choice[0]:
                            np.delete(self.__new_movies[-1], k, 0)
                            break

                    # hack: exp_data update system in the article didn't make sense for our case, which we adjusted here
                    # update exp_data of the low_freq items and after_total_exp_data of all items
                    self.__new_movies[-1][2] -= self.__new_movies[-1][2] / self.__k_neighbours
                    self.__update_total_exp(j)
                elif is_chosen:
                    # add item to output items
                    # todo: updated indices with names
                    output_item = np.array([(self.__new_movies[j][0], self.__new_movies[j][1])],
                                           dtype=[('movie_id', np.int32), ('similarity', np.float32)])
                    if output is None:
                        output = np.array(output_item)
                    else:
                        output = np.append(output, output_item)

                    # update after_total_exp data values of elements up to chosen index
                    self.__update_total_exp(j)

                    # remove chosen element from array
                    self.__new_movies = np.delete(self.__new_movies, j, 0)

                    is_picked = True

                j = j + 1

        print output  # todo: use Logger class
        return output

    def __sampling_weighted_random(self):
        raise NotImplementedError

    def __perturbation(self, movies):
        scale = 2 * self.__k_neighbours * self.__sensitivity / self.__epsilon
        for i in range(len(movies)):
            movies[i][1] = movies[i][1] + np.random.laplace(scale=scale)

    # ==================================================================================================================
    # Public
    # ==================================================================================================================
    def get_exponential_recommendation_order(self, movies, sampling_type='bernoulli'):
        """
        Generates differentially private order of movies according to their similarities using exponential mechanism
        :param movies: Array of movies which will be reordered differentially privately according to their similarity
                    values.
        :param sampling_type: Identifies the sampling method. Can be bernoulli or weighted. Default is bernoulli as its
                    implemented in the article. Weighted version has lower time complexity thus faster.
        :type sampling_type: str
        :return: Differentially privately reordered array of movies with noisy data according to their similarity values
        """
        self.__pre_processing(movies)
        if sampling_type == 'bernoulli':
            sampled = self.__sampling_bernoulli()
        elif sampling_type == 'weighted':
            sampled = self.__sampling_weighted_random()
        else:
            msg = 'Unexpected sampling type: "' + sampling_type + '"'
            print msg  # todo: use Logger Class
            raise ValueError(msg)

        self.__perturbation(sampled)
        return sampled
