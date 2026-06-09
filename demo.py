import streamlit as st
import traceback

st.write("Before import")

try:
    import recommender_model
    st.success("Import succeeded")
except Exception as e:
    st.error(f"Import failed: {e}")
    st.code(traceback.format_exc())