import streamlit as st
import pandas as pd
import plotly.express as px
from movies.service import MovieService


def show_stats():
    movie_service = MovieService()
    movie_stats = movie_service.get_movies_stats()

    genre_movies_df = pd.DataFrame(movie_stats["movies_per_genre"])

    st.header("Welcome to the Stats Section")
    st.subheader(
        "Here you can find various statistics about the movies."
    )

    st.subheader("Movie Statistics")

    if len(genre_movies_df) > 0:
        fig = px.bar(
            genre_movies_df,
            x='genre__name',
            y='count',
            labels={
                'genre__name': 'Genre',
                'count': 'Number of Movies'
            },
            title='Movies per Genre'
        )
        st.plotly_chart(fig, use_container_width=True)

    st.write("Total Movies:", movie_stats["total_movies"])

    st.write("Total Reviews:", movie_stats["total_reviews"])

    st.write("Average Rating:", movie_stats["average_rating"])
