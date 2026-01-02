import streamlit as st
from genres.repository import GenreRepository


class GenreService:

    def __init__(self):
        self.__repository = GenreRepository()

    def get_genres(self):
        if 'genres' in st.session_state:
            return st.session_state.genres
        genres = self.__repository.get_genres()
        st.session_state.genres = genres
        return genres

    def get_genre(self, genre_id):
        return self.__repository.get_genre(genre_id)

    def create_genre(self, name, description=None):
        genre = dict(
            name=name,
            description=description if description else ""
        )

        new_genre = self.__repository.create_genre(genre)
        st.session_state.genres.append(new_genre)
        return new_genre

    def update_genre(self, genre_id, name, description=None, method="put"):
        genre = dict(
            name=name,
            description=description if description else ""
        )

        return self.__repository.update_genre(genre_id, genre, method)

    def delete_genre(self, genre_id):
        return self.__repository.delete_genre(genre_id)
