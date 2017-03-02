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
