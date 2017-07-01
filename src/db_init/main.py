import time

from src import db
from src import utility as util


# item - item collaborative user dependent algorithm by using adjusted cosine similarity
def item_item_collaborative_user_dependent():
    print("item_item_collaborative_user_dependent started!")
    users_rating_avg = db.get_avg_rating_of_all_user()
    movie_ids = db.get_movie_ids()
    data = []
    for movie1_index in range(0, len(movie_ids)):
        for movie2_index in range(movie1_index + 1, len(movie_ids)):
            records = db.get_by_ratings_movie_ids(movie_ids[movie1_index], movie_ids[movie2_index])
            # check records size, if it is bigger than 10 common user, then continue
            if len(records) < 10:
                print "Unsufficient Number of Data..."
                pass
            else:
                sim = util.calculate_similarity(records, users_rating_avg)
                # sim = util.calculate_similarity2(records, users_rating_avg)
                if sim != -1:  # unidentified similarity
                    pass
                    data.append({"movie1_id": movie_ids[movie1_index],
                                 "movie2_id": movie_ids[movie2_index],
                                 "point": sim})
                    # print movie1_id, movie2_id, sim
                    if len(data) == 10000:
                        db.create_dynamic_similarity(data)
                        del data[:]
                else:
                    # divide by zero exception
                    print "divide by zero"
    # put remaining data on database
    if len(data) > 0:
        db.create_dynamic_similarity(data)
        del data[:]
    print("item_item_collaborative_user_dependent ended!")


def item_item_collaborative_user_independent():
    pass


start = time.time()

db.create_index("Movie", "movie_id")
db.create_index("User", "user_id")

db.create_movies()
# db.create_links()
db.create_ratings()
# db.create_tags()
#
# db.get_movie_by_id(1)
# db.get_avg_rating_of_movie(1)
# db.get_avg_rating_of_user(5)

item_item_collaborative_user_dependent()

end = time.time()
print "Execution time: ", end - start
