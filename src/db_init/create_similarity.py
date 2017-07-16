import time

from src.utility import similarity, db

_record_time = False


# item - item collaborative user dependent algorithm by using adjusted cosine similarity
def item_item_collaborative_user_dependent():
    print("item_item_collaborative_user_dependent started!")  # todo: use Logger Class
    users_rating_avg = db.get_avg_rating_of_all_user()
    movie_ids = db.get_movie_ids()
    data = []
    for movie1_index in range(0, len(movie_ids)):
        for movie2_index in range(movie1_index + 1, len(movie_ids)):
            records = db.get_by_ratings_movie_ids(movie_ids[movie1_index], movie_ids[movie2_index])
            # check records size, if it is bigger than 10 common user, then continue
            if len(records) < 10:
                print "Insufficient Number of Data..."  # todo: use Logger Class
            else:
                sim = similarity.calculate_similarity(records, users_rating_avg)
                # sim = similarity.calculate_similarity2(records, users_rating_avg)
                if sim != -1:  # unidentified similarity
                    data.append({"movie1_id": movie_ids[movie1_index],
                                 "movie2_id": movie_ids[movie2_index],
                                 "point": sim})
                    # print movie1_id, movie2_id, sim  # todo: use Logger Class
                    if len(data) == 10000:
                        db.create_dynamic_similarity(data)
                        del data[:]
                else:
                    # divide by zero exception
                    print "divide by zero"  # todo: use Logger Class
    # put remaining data on database
    if len(data) > 0:
        db.create_dynamic_similarity(data)
        del data[:]
    print("item_item_collaborative_user_dependent ended!")  # todo: use Logger Class


# by genres etc...
def item_item_collaborative_user_independent():
    pass


def create_similarity():
    item_item_collaborative_user_dependent()


if __name__ == '__main__':
    if _record_time:
        start = time.time()

    create_similarity()

    if _record_time:
        end = time.time()
        print(end - start)  # todo: use Logger Class
