import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

st.set_page_config("Spotify Analytics", layout="wide")

def load_css(file_name):
    with open(file_name, "r", encoding="utf-8"):
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("spotify.css")

def load_data():
    df = pd.read_csv("spotify.csv")

    df.drop_duplicates(inplace=True)

    median_dur = df["duration"].median()
    df["duration"] = df["duration"].fillna(median_dur)

    df = df[df["duration"] >= 60]

    df["language"] = df["language"].fillna("Unknown")
    df["collaboration"] = df["collaboration"].fillna("No Collaboration")


    df.rename(columns={
        "song_id": "track_id",
        "song_title": "track_name",
        "genre": "track_genre",
        "stream": "streams",
        "explicit_content": "explicit_raw"
    }, inplace=True)


    df["explicit"] = df["explicit_raw"].map({"Yes": True, "No": False})

    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["release_year"] = df["release_date"].dt.year

    df = df.dropna(subset=["release_year"])

    str_cols = df.select_dtypes(include="object").columns
    for col in str_cols:
        df[col] = df[col].str.strip()

    return df

df = load_data()

with st.sidebar:
    selected = option_menu("Main Menu",
                           ["Dataset", "Overview", "Track Analytics"],
                           icons=["table", "bar-chart", "music-note-list"],
                           menu_icon="spotify",
                           default_index=0)

# ---------------- DATASET ----------------
if selected == "Dataset":
    st.title("Data Explorer")
    st.divider()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Missing Value", df.isna().sum().sum())

    st.divider()

    st.subheader("Select Column")
    selected_column = st.multiselect("Select Column to Display",
                                     df.columns, default=df.columns)
    filtered_df = df[selected_column]

    st.subheader("Search in Dataset")
    search_value = st.text_input("Enter Value to Search")
    if search_value:
        filtered_df = filtered_df[filtered_df.astype(str).apply(
            lambda row: row.str.contains(search_value, case=False).any(), axis=1
        )]

    st.subheader("Select Row Range")
    row_range = st.slider(
        "Choose row range",
        0,
        len(filtered_df),
        (0, min(100, len(filtered_df)))
    )
    filtered_df = filtered_df.iloc[row_range[0]:row_range[1]]

    col1, col2 = st.columns(2)

    with col1:
        selected_col = st.selectbox(
            "Select Column",
            filtered_df.columns
        )

    with col2:
        unique_values = ["All"] + list(filtered_df[selected_col].dropna().unique())
        selected_value = st.selectbox(
            "Select Value",
            unique_values
        )

    if selected_value != "All":
        filtered_df = filtered_df[filtered_df[selected_col] == selected_value]

    st.dataframe(filtered_df, use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Filtered Data",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv"
    )

# ---------------- OVERVIEW ----------------
if selected == "Overview":
    st.header("Track Overview")

    total_tracks = len(df)
    total_streams = df["streams"].sum()
    avg_popularity = df["popularity"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Tracks", total_tracks)
    col2.metric("Total Streams", f"{total_streams:,.0f}")
    col3.metric("Avg Popularity", f"{avg_popularity:.1f}")
    col4.metric("Avg Duration (sec)", f"{df['duration'].mean():.0f}s")

    st.divider()

# ---------------- ANALYTICS ----------------

if selected == "Track Analytics":
    st.title("Advance Track Intelligence Dashboard")

    high_pop = df[df["popularity"] >= 70]

    # LINE CHART
    st.subheader("Total Streams by Release Year")
    streams_year = df.groupby("release_year")["streams"].sum().reset_index()

    fig1 = px.line(streams_year,
                   x="release_year",
                   y="streams",
                   markers=True,
                   title="Total Streams Trend (1994–2024)",
                   color_discrete_sequence=["#1DB954"])
    fig1.update_layout(height=420)
    st.plotly_chart(fig1, use_container_width=True)

    # SUNBURST CHART
    st.subheader("High Popularity Tracks: Genre → Label Hierarchy")

    fig2 = px.sunburst(high_pop,
                       path=["track_genre", "label"],
                       values="streams",
                       color="streams",
                       color_continuous_scale="Turbo")

    fig2.update_layout(height=520)
    st.plotly_chart(fig2, use_container_width=True)
    with st.container(border=True):
        bar_chart = df.groupby("track_genre")["streams"].mean().reset_index().sort_values(by="streams",
                                                                                          ascending=False).head(10)

        fig3 = px.bar(
            bar_chart,
            x="track_genre",
            y="streams",
            color="track_genre",
            title="Top Genres by Average Streams"
        )

        st.plotly_chart(fig3, use_container_width=True)

    barh_chart = df["track_genre"].value_counts().head(10)

    fig4 = px.bar(
        barh_chart,
        y=barh_chart.index,
        x=barh_chart.values,
        orientation='h',
        title="Top 10 Genres by Track Count",
        color=barh_chart.index
    )

    st.plotly_chart(fig4, use_container_width=True)
    with st.container(border=True):
        # sankey diagram
        st.subheader("Music Flow Analysis (Genre → Language)")
        flow = df.groupby(["track_genre", "language"]).size().reset_index(name="Count")

        source_label = flow["track_genre"].unique().tolist()
        target_label = flow["language"].unique().tolist()

        labels = source_label + target_label
        source = flow["track_genre"].apply(
            lambda x: labels.index(x)
        )
        target = flow["language"].apply(
            lambda x: labels.index(x)
        )

        value = flow["Count"].tolist()
        import plotly.graph_objects as go
        fig4 = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="blue", width=0.5),
                label=labels
            ),
            link=dict(
                source=source,
                target=target,
                value=value
            )
        )])
        st.plotly_chart(fig4, use_container_width=True)