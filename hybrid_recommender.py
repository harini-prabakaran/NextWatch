import pandas as pd

from recommender_model import (
    cosine_matrix,
    genre_similarity
)


def recommend_hybrid(
    movie_name,
    top_n=10
):

    if movie_name not in cosine_matrix:
        return []

    collab = cosine_matrix[movie_name]
    content = genre_similarity[movie_name]

    collab = (
        collab - collab.min()
    ) / (
        collab.max() - collab.min()
    )

    content = (
        content - content.min()
    ) / (
        content.max() - content.min()
    )

    score = (
        0.7 * collab
        + 0.3 * content
    )

    return (
        score
        .drop(movie_name, errors="ignore")
        .nlargest(top_n)
        .index
        .tolist()
    )