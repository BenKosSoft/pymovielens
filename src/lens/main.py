import math
import time

from src import db


# item - item collaborative user dependent algorithm by using adjusted cosine similarity
def item_item_collaborative_user_dependent():
    print("item_item_collaborative_user_dependent started!")
    users_rating_avg = db.get_avg_rating_of_all_user()
    movie_ids = db.get_movie_ids()
    data = []
    for movie1_index in range(0, len(movie_ids)):
        for movie2_index in range(movie1_index+1, len(movie_ids)):
            records = db.get_by_ratings_movie_ids(movie_ids[movie1_index], movie_ids[movie2_index])
            # check records size, if it is bigger than 10 common user, then continue
            if len(records) < 10:
                print "Unsufficient Number of Data..."
                pass
            else:
                a, b, c = 0, 0, 0
                for record in records:
                    rating1 = record["rating1"]
                    rating2 = record["rating2"]
                    user_id = record["user_id"]
                    user_rating_mean = users_rating_avg.get(user_id, None)
                    if user_rating_mean is None:
                        continue
                    d = (rating1-user_rating_mean)
                    e = (rating2-user_rating_mean)
                    a += d*e
                    b += d*d
                    c += e*e
                if b != 0 and c != 0:
                    sim = a / (math.sqrt(b)*math.sqrt(c))
                    data.append({"movie1_id": movie_ids[movie1_index],
                                 "movie2_id": movie_ids[movie2_index],
                                 "point": sim})
                    # print movie1_id, movie2_id, sim
                    if len(data) == 10000:
                        db.create_dynamic_similarity(data)
                        del data[:]
                else:
                    # divide by zero exception
                    pass
    # put remaining data on database
    if len(data) > 0:
        db.create_dynamic_similarity(data)
        del data[:]
    print("item_item_collaborative_user_dependent ended!")


def func2():
    pass

start = time.time()


# db.create_index("Movie", "movie_id")
# db.create_index("User", "user_id")
#
# db.create_movies()
# db.create_links()
# db.create_ratings()
# db.create_tags()
#
# db.get_movie_by_id(1)
# db.get_avg_rating_of_movie(1)
# db.get_avg_rating_of_user(5)

item_item_collaborative_user_dependent()

end = time.time()
print "Execution time: ", end-start
