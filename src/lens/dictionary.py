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
movie_csv = "../../res_unshared/ml-latest-small/movies.csv"
rating_csv = "../../res_unshared/ml-latest-small/ratings.csv"
link_csv = "../../res_unshared/ml-latest-small/links.csv"
tag_csv = "../../res_unshared/ml-latest-small/tags.csv"
movie_query_get_by_id = "MATCH (m:Movie) " \
                  "WHERE m.movie_id = {movie_id}" \
                  "RETURN m"
index_query_create = "CREATE INDEX ON :{}({})"
movie_query_get_avg_rating = "MATCH (m:Movie)<-[r:rates]-(u:User)" \
                             "WHERE m.movie_id = {movie_id}" \
                             "RETURN m.title AS title, AVG(r.rating) AS rating_avg"
user_query_get_avg_rating = "MATCH (m:Movie)<-[r:rates]-(u:User)" \
                            "WHERE u.user_id = {user_id}" \
                            "RETURN u.user_id, AVG(r.rating) AS rating_avg"
movie_query_get_all = "MATCH (m:Movie)<-[r:rates]-(u:User)" \
                             "RETURN m.movie_id, m.genres"
movie_query_create_static_similarity = "UNWIND {data} as d " \
                      "MATCH (m1:Movie {movie_id:d.movie1_id}) " \
                      "MATCH (m2:Movie {movie_id:d.movie2_id}) " \
                      "MERGE (m1)-[:static_sim {point:d.point}]-(m2)"
movie_query_create_dynamic_similarity = "UNWIND {data} as d " \
                      "MATCH (m1:Movie {movie_id:d.movie1_id}) " \
                      "MATCH (m2:Movie {movie_id:d.movie2_id}) " \
                      "MERGE (m1)-[:dynamic_sim {point:d.point}]-(m2)"
