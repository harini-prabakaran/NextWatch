import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

print("STEP 1")

movies = pd.read_csv("data/movies.csv")
print("STEP 2")

ratings = pd.read_csv("data/ratings.csv")
print("STEP 3")

genre_matrix = movies["genres"].str.get_dummies("|")
print("STEP 4")

genre_similarity = pd.DataFrame(
    cosine_similarity(genre_matrix),
    index=movies["title"],
    columns=movies["title"]
)
print("STEP 5")

movie_ratings = pd.merge(ratings, movies, on="movieId")
print("STEP 6")

movie_stats = movie_ratings.groupby("title")["rating"].agg(["mean", "count"])
print("STEP 7")

user_movie_matrix = movie_ratings.pivot_table(
    index="userId",
    columns="title",
    values="rating"
)
print("STEP 8")

movie_vectors = user_movie_matrix.fillna(0).T
print("STEP 9")

pearson_matrix = user_movie_matrix.corr(
    method="pearson",
    min_periods=5
)
print("STEP 10")

cosine_matrix = pd.DataFrame(
    cosine_similarity(movie_vectors),
    index=movie_vectors.index,
    columns=movie_vectors.index
)
print("STEP 11")