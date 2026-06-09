import streamlit as st

from recommender_model import user_movie_matrix

st.title("Test")
st.write(user_movie_matrix.shape)