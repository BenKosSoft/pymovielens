import numpy as np
from src.utility import db


class LaplaceMechanism:
    """
    Laplace mechanism for differentially private applications
    """

    # ==================================================================================================================
    # Private
    # ==================================================================================================================
    def __init__(self, sensitivity=1, epsilon=0.1):
        """
        Initialize privatization parameters to apply laplace mechanism functionalities
        :param sensitivity:  Sensitivity coefficient
        :param epsilon:      Epsilon value for, epsilon-differentially private queries
        """
        self.__sensitivity = sensitivity
        self.__epsilon = epsilon
        self.__scale = self.__sensitivity / self.__epsilon
        self.__rand = np.random

    # ==================================================================================================================
    # Public
    # ==================================================================================================================
    def get_private_count(self, movie_id):
        movie_rating_count = db.get_movie_rating_count(movie_id)
        noisy_count = self.__rand.laplace(scale=self.__scale) + movie_rating_count
        return movie_rating_count, noisy_count
