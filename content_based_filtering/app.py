import streamlit as st
import pickle
import requests
import gzip

st.set_page_config(page_title="Movie Recommender System", layout="wide")

st.markdown(
    """
    <style>
    body {
        background-color: #000000;
        color: white;
    }
    .stApp {
        background-color: #000000;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=7006be7f564f4723e00a7b6b5138c21a&language=en-US"
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    matches = movies[movies['title'] == movie]
    if matches.empty:
        return [], []
    movie_index = matches.index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_poster.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_poster

# Load data
with gzip.open('similarity_matrix.pkl.gz','rb')as f:
    similarity=pickle.load(f)
movies = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies['title'].values

# Title
st.title("Movie Recommender System")

# Columns for narrow input
col1, col2 = st.columns([1, 5])
with col1:
    option = st.selectbox("Select a movie to get recommendations", movies_list)
    recommend_button = st.button("Recommend")

# Recommendation output
if recommend_button:
    recommendation, poster = recommend(option)
    if recommendation:
        cols = st.columns(5)
        for i in range(len(recommendation)):
            with cols[i]:
                st.text(recommendation[i])
                st.image(poster[i])
    else:
        st.error("Sorry, no recommendations found for the selected movie.")
