import streamlit as st
import pandas as pd
from datetime import datetime
# from st_aggrid import AgGrid
from actors.service import ActorService
from genres.service import GenreService
from movies.service import MovieService


def show_movies():
    movie_service = MovieService()
    movies = movie_service.get_movies()

    if not movies:
        st.warning("No movies found or unauthorized access.")
        st.button(
            "Create Movie",
            on_click=create_movie,
            key="create_movie"
        )
        return
    else:
        st.header("Welcome to the List of Movies")
        df_movies = pd.json_normalize(movies)

        st.button(
            "Create Movie",
            on_click=create_movie,
            key="create_movie"
        )

        for _, movie in df_movies.iterrows():

            actor_list = movie.get('actors', [])
            actors_names = [
                actor.get('name', str(actor)) for actor in actor_list
            ]
            actors_str = ", ".join(actors_names) if actors_names else "—"

            tile = st.container(border=True)
            tile.markdown(
                f"### {movie['title']}"
            )
            tile.markdown(
                f"**Genre:** {movie.get('genre.name', 'N/A')}"
            )
            tile.markdown(
                f"**Description:** {movie.get('description', 'N/A')}"
            )
            tile.markdown(
                f"**Release Date:** {movie.get('release_date', 'N/A')}"
            )
            tile.markdown(
                f"**Duration:** {movie.get('duration', 'N/A')} min"
            )
            tile.markdown(
                f"**Actors:** {actors_str}"
            )
            movie_update, movie_delete = tile.columns(2, gap=None)
            movie_update.button(
                "Edit",
                on_click=update_movie,
                args=(movie['id'],),
                key=f"edit_{movie['id']}"
            )
            movie_delete.button(
                "Delete",
                on_click=delete_movie,
                args=(movie['id'],),
                key=f"delete_{movie['id']}"
            )


@st.dialog("Create Movie")
def create_movie():
    movie_service = MovieService()
    genres = GenreService().get_genres()
    actors = ActorService().get_actors()

    st.subheader("Submit new Movie")

    title = st.text_input("Movie Title")
    genre = {genre["name"]: genre["id"] for genre in genres}
    selected_genre = st.selectbox(
        "Genre",
        options=list(genre.keys()),
    )
    description = st.text_area("Description")
    release_date = st.date_input(
        label="Release Date",
        value=datetime.today(),
        min_value=datetime(1900, 1, 1),
        format="DD/MM/YYYY"
    )

    duration = st.number_input("Duration (minutes)", min_value=1)
    actor = {actor["name"]: actor["id"] for actor in actors}
    selected_actor = st.multiselect(
        "Actors",
        options=list(actor.keys()),
        default=[]
    )
    selected_actor_ids = [actor[actor_name] for actor_name in selected_actor]

    if st.button("Submit"):
        new_movie = movie_service.create_movie(
            title=title,
            genre=genre[selected_genre],
            description=description,
            release_date=release_date,
            duration=duration,
            actors=selected_actor_ids
        )
        if new_movie:
            st.success(f"Movie '{title}' added successfully!")
            st.rerun()
        else:
            st.error("Failed to add movie. Please try again.")


@st.dialog("Update Movie")
def update_movie(movie_id):
    movie_service = MovieService()
    genres = GenreService().get_genres()
    actors = ActorService().get_actors()
    movie = movie_service.get_movie(movie_id=movie_id)

    if not movie:
        st.error("Movie not found or unauthorized access.")
        return

    st.subheader(f"Update Movie: {movie['title']}")
    title = st.text_input("Movie Title", value=movie['title'])
    genre = {genre["name"]: genre["id"] for genre in genres}
    selected_genre = st.selectbox(
        "Genre",
        options=list(genre.keys())
    )
    description = st.text_area(
        "Description",
        value=movie.get('description', '')
    )
    release_date = st.date_input(
        label="Release Date",
        value=datetime.today(),
        min_value=datetime(1900, 1, 1),
        format="DD/MM/YYYY"
    )
    duration = st.number_input(
        "Duration (minutes)",
        min_value=1,
        value=movie.get('duration', 1)
    )
    actor = {actor["name"]: actor["id"] for actor in actors}
    selected_actor = st.multiselect(
        "Actors",
        options=list(actor.keys()),
        default=[
            actor["name"] for actor in actors
            if actor["id"] in movie.get('actors', [])
        ]
    )
    selected_actor_ids = [actor[actor_name] for actor_name in selected_actor]

    if st.button("Update"):
        updated_movie = movie_service.update_movie(
            movie_id=movie_id,
            title=title,
            genre=genre[selected_genre],
            description=description,
            release_date=release_date,
            duration=duration,
            actors=selected_actor_ids
        )
        if updated_movie:
            st.success(f"Movie '{title}' updated successfully!")
            st.rerun()
        else:
            st.error("Failed to update movie. "
                     "Check your input or session state.")


@st.dialog("Delete Movie")
def delete_movie(movie_id):
    movie_service = MovieService()
    movie = movie_service.get_movie(movie_id=movie_id)

    if not movie:
        st.error("Movie not found or unauthorized access.")
        return

    st.subheader(f"Delete Movie: {movie['title']}")
    if st.button("Confirm Delete"):
        st.success(f"Movie '{movie['title']}' deleted successfully!")
        st.rerun()
    else:
        st.error("Failed to delete movie. "
                 "Check your input or session state.")
        return
