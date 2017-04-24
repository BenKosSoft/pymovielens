movie_query_create = "UNWIND {data} as d " \
             "MERGE (m:Movie {movie_id:d.movie_id, title:d.title, genres:d.genres})"
link_query_create = "UNWIND {data} as d " \
            "MATCH (m:Movie {movie_id:d.movie_id}) " \
            "SET m.imdbId = d.imdbId, m.tmdbId = d.tmdbId"
rating_query_create = "UNWIND {data} as d MATCH (m:Movie {movie_id:d.movie_id}) " \
              "MERGE (u:User {user_id:d.user_id}) " \
              "MERGE (u)-[:rates {rating:d.rating, time:d.timestamp}]->(m)"
tag_query_create = "UNWIND {data} as d " \
           "MATCH (m:Movie {movie_id:d.movie_id}) " \
           "MATCH (u:User {user_id:d.user_id}) " \
           "MERGE (u)-[:tags {tag:d.tag, time:d.timestamp}]->(m)"
movie_csv = "../../res_unshared/ml-mini/movies.csv"
rating_csv = "../../res_unshared/ml-mini/ratings_train_0.8.csv"
link_csv = "../../res_unshared/ml-latest-small/links.csv"
tag_csv = "../../res_unshared/ml-latest-small/tags.csv"
movie_query_get_by_id = "MATCH (m:Movie) " \
                  "WHERE m.movie_id = {movie_id}" \
                  "RETURN m"
index_query_create = "CREATE INDEX ON :{}({})"
movie_query_get_avg_rating = "MATCH (m:Movie)<-[r:rates]-(u:User)" \
                             "WHERE m.movie_id = {movie_id}" \
                             "RETURN m.title AS title, AVG(r.rating) AS rating_avg"
user_query_get_avg_rating = "MATCH (m:Movie)<-[r:rates]-(u:User) " \
                            "WHERE u.user_id = {user_id} " \
                            "RETURN u.user_id as user_id, AVG(r.rating) AS rating_avg"
user_query_get_all_avg_rating = "MATCH (m:Movie)<-[r:rates]-(u:User) " \
                                "RETURN u.user_id as user_id, ROUND(10 * AVG(r.rating)) / 10 AS rating_avg"
movie_query_get_all = "MATCH (m:Movie)" \
                             "RETURN m.movie_id as movie_id, m.genres as genres"
movie_query_create_static_similarity = "UNWIND {data} as d " \
                      "MATCH (m1:Movie {movie_id:d.movie1_id}) " \
                      "MATCH (m2:Movie {movie_id:d.movie2_id}) " \
                      "MERGE (m1)-[:static_sim {point:d.point}]-(m2)"
movie_query_create_dynamic_similarity = "UNWIND {data} as d " \
                      "MATCH (m1:Movie {movie_id:d.movie1_id}) " \
                      "MATCH (m2:Movie {movie_id:d.movie2_id}) " \
                      "MERGE (m1)-[:dynamic_sim {point:d.point}]-(m2)"
movie_movie_query_adjusted_cosine = "MATCH (m1:Movie)<-[r1:rates]-(u:User)-[r2:rates]->(m2:Movie) " \
                                    "WHERE m1.movie_id = {movie1_id} AND m2.movie_id = {movie2_id} " \
                                    "RETURN r1.rating as rating1, u.user_id as user_id, r2.rating as rating2"
movie_query_get_all_movie_ids = "MATCH (m:Movie)" \
                      "RETURN m.movie_id as movie_id"
movie_query_get_similarities_by_movie = "MATCH (m1:Movie)-[ds:dynamic_sim]-(m2:Movie) " \
                                        "WHERE m1.movie_id = {movie_id} " \
                                        "RETURN m2.movie_id as other_movie_id, ds.point as similarity"
user_query_get_ratings_of_user = "MATCH (u:User)-[r:rates]->(m:Movie) " \
                                 "WHERE u.user_id = {user_id} " \
                                 "RETURN m.movie_id as movie_id, r.rating as rating"
