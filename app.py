import streamlit as st

from recommender_model import (
    user_movie_matrix,
    recommend_cosine
)

from hybrid_recommender import (
    recommend_hybrid
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="NextWatch AI",
    page_icon="🎬",
    layout="wide"
)
st.markdown("""
<style>

/* =========================
   GLOBAL THEME
========================= */

.stApp {
    background:
    linear-gradient(
        135deg,
        #0f172a 0%,
        #111827 50%,
        #000000 100%
    );
}

/* Hide Streamlit branding */

#MainMenu,
footer,
header {
    visibility: hidden;
}

/* =========================
   TITLE
========================= */

h1 {
    text-align: center;
    color: white !important;
    font-size: 3rem !important;
}

p {
    color: #d1d5db;
}

/* =========================
   TABS
========================= */

[data-baseweb="tab-list"] {
    gap: 12px;
}

[data-baseweb="tab"] {
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 12px 24px;
    color: white;
    font-weight: 600;
    transition: all 0.3s ease;
}

[data-baseweb="tab"]:hover {
    background: rgba(229,9,20,0.25);
    transform: translateY(-2px);
}

/* =========================
   BUTTONS
========================= */

.stButton button {
    background: linear-gradient(
        135deg,
        #e50914,
        #b20710
    );

    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 1.5rem;

    font-weight: bold;

    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: scale(1.03);
    box-shadow:
        0px 0px 20px
        rgba(229,9,20,0.5);
}

/* =========================
   SELECT BOXES
========================= */

.stSelectbox {
    border-radius: 12px;
}

/* =========================
   INFO BOXES
========================= */

[data-testid="stAlert"] {
    border-radius: 15px;
}

/* =========================
   MOVIE CARDS
========================= */

.movie-card {

    background:
    rgba(255,255,255,0.06);

    border-radius: 15px;

    padding: 16px;

    margin-top: 10px;
    margin-bottom: 10px;

    border:
    1px solid rgba(
        255,255,255,0.08
    );

    transition: all 0.3s ease;

    animation:
    fadeIn 0.6s ease forwards;
}

.movie-card:hover {

    transform:
    translateY(-4px);

    background:
    rgba(229,9,20,0.15);

    box-shadow:
    0 10px 25px rgba(
        229,
        9,
        20,
        0.25
    );
}

.movie-title {
    color: white;
    font-size: 18px;
    font-weight: 600;
}

/* =========================
   HERO BANNER
========================= */

.hero {

    padding: 30px;

    border-radius: 20px;

    background:
    linear-gradient(
        135deg,
        #e50914,
        #b20710
    );

    text-align: center;

    margin-bottom: 25px;

    animation:
    fadeIn 1s ease;
}

.hero h2 {
    color: white;
}

.hero p {
    color: #f3f4f6;
}

/* =========================
   ANIMATION
========================= */

@keyframes fadeIn {

    from {
        opacity: 0;
        transform:
        translateY(10px);
    }

    to {
        opacity: 1;
        transform:
        translateY(0px);
    }
}
/* =========================
   NETFLIX MOVIE ROW
========================= */

.movie-row {

    display: flex;

    overflow-x: auto;

    gap: 16px;

    padding: 10px 0 20px 0;

    scrollbar-width: none;
}

.movie-row::-webkit-scrollbar {
    display: none;
}

.movie-card-netflix {

    min-width: 220px;

    height: 130px;

    border-radius: 16px;

    background:
    linear-gradient(
        135deg,
        rgba(229,9,20,0.8),
        rgba(255,255,255,0.08)
    );

    display: flex;

    align-items: center;
    justify-content: center;

    text-align: center;

    color: white;

    font-weight: 600;

    font-size: 15px;

    padding: 12px;

    flex-shrink: 0;

    transition: all 0.3s ease;
}

.movie-card-netflix:hover {

    transform: scale(1.08);

    cursor: pointer;

    box-shadow:
        0 10px 25px
        rgba(229,9,20,0.35);
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# DATA
# --------------------------------------------------

all_movies = sorted(
    user_movie_matrix.columns.tolist()
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🎬 NextWatch AI")

st.caption(
    """
    Find your next favorite movie through intelligent
    recommendations tailored to your interests.
    """
)

st.divider()

# --------------------------------------------------
# RECOMMENDATIONS
# --------------------------------------------------

st.subheader(
    "🍿 Find Your Next Movie"
)

selected_movie = st.selectbox(
    "Choose a Movie",
    all_movies
)

if st.button(
    "Find Recommendations",
    use_container_width=True
):

    with st.spinner(
        "🍿 Finding great movies for you..."
    ):

        collaborative = recommend_cosine(
            selected_movie
        )

        hybrid = recommend_hybrid(
            movie_name=selected_movie
        )

    # ==================================
    # VIEWERS ALSO ENJOYED
    # ==================================

    st.markdown("---")

    

    st.markdown(
        f"### People Who Enjoyed '{selected_movie}' Also Enjoyed"
    )
    st.caption(
        """
        Movies that are frequently enjoyed by
        viewers who liked the same movie.
        """
    )

    cards_html = ""

    import urllib.parse

    for movie in collaborative.index:

        search_url = (
            "https://www.google.com/search?q="
            + urllib.parse.quote(movie + " movie")
        )

        cards_html += f"""
        <a href="{search_url}" target="_blank"
            style="text-decoration:none; color:white; ">
            <div class="movie-card-netflix">
                {movie}
            </div>
        </a>
        """

    st.markdown(
        f"""
        <div class="movie-row">
            {cards_html}
        </div>
        """,
        unsafe_allow_html=True
    )

    # ==================================
    # RECOMMENDED FOR YOU
    # ==================================

    st.markdown("---")

    st.markdown(
        f"### Recommended for you "
    )
    
    st.caption(
        """
        Recommendations based on movie themes,
        genres, and viewer preferences.
        """
    )

    cards_html = ""

    for movie in hybrid:

        search_url = (
            "https://www.google.com/search?q="
            + urllib.parse.quote(movie + " movie")
        )

        cards_html += f"""
        <a href="{search_url}" target="_blank"
            style="text-decoration:none; color:white; ">
            <div class="movie-card-netflix">
                {movie}
            </div>
        </a>
        """

    st.markdown(
        f"""
        <div class="movie-row">
            {cards_html}
        </div>
        """,
        unsafe_allow_html=True
    )

    

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    """
    Disclaimer: Recommendations are generated using historical movie ratings
    and similarity patterns. Results are intended for discovery and entertainment
    purposes and may not reflect every user's personal preferences.
    """
)