import streamlit as st
from movies.repository import MovieRepository


class MovieService:

    def __init__(self):
        self.repository = MovieRepository()

    def get_movies(self):
        if 'movies' in st.session_state:
            return st.session_state.movies
        movies = self.repository.get_movies()
        st.session_state.movies = movies
        return movies

    def get_movie(self, movie_id):
        return self.repository.get_movie(movie_id)

    def create_movie(
            self,
            title,
            genre,
            description,
            release_date,
            duration,
            actors=None
    ):
        if actors is None:
            actors = []
        movie = dict(
            title=title,
            genre=genre,
            description=description if description else "",
            release_date=release_date,
            duration=duration,
            actors=actors
        )

        new_movie = self.repository.create_movie(movie)
        st.session_state.movies.append(new_movie)
        return new_movie

    def update_movie(
            self,
            movie_id,
            title,
            genre,
            description,
            release_date,
            duration,
            actors=None
    ):
        if actors is None:
            actors = []
        movie = dict(
            title=title,
            genre=genre,
            description=description if description else "",
            release_date=release_date,
            duration=duration,
            actors=actors
        )

        return self.repository.update_movie(movie_id, movie)

    def delete_movie(self, movie_id):
        return self.repository.delete_movie(movie_id)

    def get_movies_stats(self):
        return self.repository.get_movies_stats()
