import numpy as np
import pandas as pd
import tensorflow as tf


def train_matrix_factorization(
    min_ratings=50,
    num_features=20,
    lambda_=0.5,
    epochs=100,
    learning_rate=0.01,
):
    movies = pd.read_csv("data/movies.csv")
    ratings = pd.read_csv("data/ratings.csv")

    movie_ratings = pd.merge(ratings, movies, on="movieId")

    user_movie_matrix = movie_ratings.pivot_table(
        index="userId",
        columns="title",
        values="rating"
    )

    popular_movies = (
        movie_ratings["title"]
        .value_counts()
        .loc[lambda x: x > min_ratings]
        .index
    )

    Y_df = user_movie_matrix[popular_movies]
    R = Y_df.notna().astype(int).values
    Y = Y_df.fillna(0).values

    np.random.seed(42)
    test_mask = (R == 1) & (np.random.rand(*R.shape) < 0.2)

    train_R = R.copy()
    train_R[test_mask] = 0

    num_users, num_movies = Y.shape

    tf.random.set_seed(42)

    X = tf.Variable(
        tf.random.normal([num_movies, num_features], stddev=0.1)
    )
    W = tf.Variable(
        tf.random.normal([num_users, num_features], stddev=0.1)
    )
    b = tf.Variable(tf.zeros([num_users, 1]))

    Y_tf = tf.constant(Y, dtype=tf.float32)
    train_R_tf = tf.constant(train_R, dtype=tf.float32)

    optimizer = tf.keras.optimizers.Adam(
        learning_rate=learning_rate
    )

    for _ in range(epochs):
        with tf.GradientTape() as tape:
            predictions = tf.matmul(W, X, transpose_b=True) + b
            error = (predictions - Y_tf) * train_R_tf

            cost = (
                0.5 * tf.reduce_sum(tf.square(error))
                + (lambda_ / 2) * (
                    tf.reduce_sum(tf.square(W))
                    + tf.reduce_sum(tf.square(X))
                )
            )

        grads = tape.gradient(cost, [X, W, b])
        optimizer.apply_gradients(zip(grads, [X, W, b]))

    final_predictions = (
        tf.matmul(W, X, transpose_b=True) + b
    ).numpy()

    train_rmse = np.sqrt(
        np.mean(
            (final_predictions[train_R == 1] - Y[train_R == 1]) ** 2
        )
    )

    test_rmse = np.sqrt(
        np.mean(
            (final_predictions[test_mask] - Y[test_mask]) ** 2
        )
    )

    return final_predictions, train_rmse, test_rmse, Y_df, R


(    FINAL_PREDICTIONS,
    TRAIN_RMSE,
    TEST_RMSE,
    Y_DF,
    R_MATRIX
) = train_matrix_factorization()

def recommend_mf(user_id, top_n=10):
    idx = user_id - 1

    return (
        pd.Series(FINAL_PREDICTIONS[idx], index=Y_DF.columns)
        .drop(Y_DF.columns[R_MATRIX[idx] == 1], errors="ignore")
        .nlargest(top_n)
    )