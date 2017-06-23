import math
from sklearn.metrics.pairwise import cosine_similarity as cs
import numpy as np


# This functions calculate similarity by our implementation
def calculate_similarity(records, averages):
    a, b, c = calculate_similarity_values(records, averages)
    if b != 0 and c != 0:
        sim = a / (math.sqrt(b) * math.sqrt(c))
        return normalize_similarity(sim)
    else:
        return -1


def calculate_similarity_values(records, averages):
    a, b, c = 0, 0, 0
    for record in records:
        rating1 = record["rating1"]
        rating2 = record["rating2"]
        user_id = record["user_id"]
        user_rating_mean = averages.get(user_id, None)
        if user_rating_mean is None:
            continue
        d = (rating1 - user_rating_mean)
        e = (rating2 - user_rating_mean)
        a += d * e
        b += d * d
        c += e * e
    return a, b, c


# This functions calculate similarity by default functions
def calculate_similarity2(records, users_rating_avg):
    x, y, n = calculate_similarity_values2(records, users_rating_avg)
    x = np.subtract(x, n)
    y = np.subtract(y, n)
    sim = normalize_similarity(cs([x], [y])[0][0])
    if sim == 0.5:  # it means divide by zero
        return -1
    return sim


def calculate_similarity_values2(records, averages):
    x, y, n = np.array([]), np.array([]), np.array([])
    for record in records:
        x = np.append(x, record["rating1"])
        y = np.append(y, record["rating2"])
        n = np.append(n, averages.get(record["user_id"], 0))
    return x, y, n


def normalize_similarity(sim):
    return round((sim / 2) + 0.5, 3)
