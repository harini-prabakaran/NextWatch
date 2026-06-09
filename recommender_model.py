import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("data/movies.csv")
ratings = pd.read_csv("data/ratings.csv")
genre_matrix = movies["genres"].str.get_dummies("|")

genre_similarity = pd.DataFrame(
    cosine_similarity(genre_matrix),
    index=movies["title"],
    columns=movies["title"]
)
movie_ratings = pd.merge(ratings, movies, on="movieId")
movie_stats = movie_ratings.groupby("title")["rating"].agg(["mean", "count"])

user_movie_matrix = movie_ratings.pivot_table(
    index="userId", columns="title", values="rating"
)

movie_vectors = user_movie_matrix.fillna(0).T

# pearson_matrix = user_movie_matrix.corr(method="pearson", min_periods=5)

cosine_matrix = pd.DataFrame(
    cosine_similarity(movie_vectors),
    index=movie_vectors.index,
    columns=movie_vectors.index
)

# def recommend_pearson(movie_name, min_ratings=100, top_n=10):
#     if movie_name not in pearson_matrix.columns:
#         return "Movie not found"

#     recommendations = pearson_matrix[[movie_name]].copy()
#     recommendations.columns = ["correlation"]
#     recommendations.dropna(inplace=True)
#     recommendations["count"] = movie_stats["count"].reindex(recommendations.index)

#     recommendations = recommendations[recommendations["count"] > min_ratings]
#     recommendations = recommendations.sort_values("correlation", ascending=False)
#     recommendations = recommendations.drop(movie_name, errors="ignore")

#     return recommendations.head(top_n)

def recommend_cosine(movie_name, min_ratings=100, top_n=10):
    if movie_name not in cosine_matrix.columns:
        return "Movie not found"

    recommendations = cosine_matrix[[movie_name]].copy()
    recommendations.columns = ["similarity"]
    recommendations["count"] = movie_stats["count"].reindex(recommendations.index)

    recommendations = recommendations[recommendations["count"] > min_ratings]
    recommendations = recommendations.sort_values("similarity", ascending=False)
    recommendations = recommendations.drop(movie_name, errors="ignore")

    return recommendations.head(top_n)