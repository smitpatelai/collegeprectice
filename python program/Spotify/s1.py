import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings('ignore')


# def load_css():
#     with open("spotify.css") as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
#
# load_css()

st.set_page_config(
    page_title="Spotify Analytics",
    page_icon="🎵",
    layout="wide"
)


COLORS = ['#534AB7', '#1D9E75', '#D85A30', '#D4537E',
          '#378ADD', '#639922', '#BA7517', '#E24B4A', '#888780']


@st.cache_data
def load_data():
    df = pd.read_csv("SPOTIFY - spotify_songs_dataset.csv.csv")

    # Parse dates
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    df['year'] = df['release_date'].dt.year

    # Fill missing values
    df['duration'].fillna(df['duration'].median(), inplace=True)
    df['language'].fillna('Unknown', inplace=True)

    # Collab flag
    df['has_collab'] = df['collaboration'].notna()

    return df


df = load_data()


st.sidebar.header("Filters")

all_genres = sorted(df['genre'].dropna().unique().tolist())
selected_genres = st.sidebar.multiselect("Genres", all_genres, default=all_genres)

all_langs = sorted(df['language'].dropna().unique().tolist())
selected_langs = st.sidebar.multiselect("Languages", all_langs, default=all_langs)

min_year = int(df['year'].min()) if df['year'].notna().any() else 2000
max_year = int(df['year'].max()) if df['year'].notna().any() else 2024
year_range = st.sidebar.slider("Release Year", min_year, max_year, (2010, max_year))

pop_range = st.sidebar.slider("Popularity Range", 0, 100, (0, 100))

explicit_filter = st.sidebar.radio("Explicit Content", ["All", "Yes", "No"])

# Apply filters
mask = (
    df['genre'].isin(selected_genres) &
    df['language'].isin(selected_langs) &
    df['year'].between(year_range[0], year_range[1]) &
    df['popularity'].between(pop_range[0], pop_range[1])
)
if explicit_filter != "All":
    mask &= df['explicit_content'] == explicit_filter

filtered = df[mask]
