import pandas as pd
import streamlit as st
# from st_aggrid import AgGrid
from genres.service import GenreService


def show_genres():
    genre_service = GenreService()
    genres = genre_service.get_genres()

    if not genres:
        st.warning("No genres found or unauthorized access.")
        st.button(
            "Create Genre",
            on_click=create_genre,
            key="create_genre"
        )
        return
    else:
        st.header("Welcome to the List of Genres")
        df_genres = pd.json_normalize(genres)

        st.button(
            "Create Genre",
            on_click=create_genre,
            key="create_genre"
        )

        for _, genre in df_genres.iterrows():
            tile = st.container(border=True)
            tile.markdown(f"### {genre['name']}")
            tile.markdown(
                f"**Description:** {genre.get('description', 'N/A')}"
            )
            genre_update, genre_delete = tile.columns(2, gap=None)
            genre_update.button(
                "Edit",
                on_click=update_genre,
                args=(genre['id'],),
                key=f"edit_{genre['id']}"
            )
            genre_delete.button(
                "Delete",
                on_click=delete_genre,
                args=(genre['id'],),
                key=f"delete_{genre['id']}"
            )


@st.dialog("Create Genre")
def create_genre():
    genre_service = GenreService()
    st.subheader("Submit new Genre")
    name = st.text_input("Genre Name")
    description = st.text_area("Description")

    if st.button("Submit"):
        new_genre = genre_service.create_genre(
            name=name,
            description=description,
        )
        if new_genre:
            st.success(f"Genre '{name}' added successfully!")
            st.rerun()
        else:
            st.error("Failed to add genre. Check your input or session state.")


@st.dialog("Update Genre")
def update_genre(genre_id):
    genre_service = GenreService()
    genre = genre_service.get_genre(genre_id=genre_id)

    if not genre:
        st.error("Genre not found or unauthorized access.")
        return

    st.subheader(f"Update Genre: {genre['name']}")
    name = st.text_input("Genre Name", value=genre['name'])
    description = st.text_area(
        "Description",
        value=genre.get('description', ''))

    if st.button("Update"):
        updated_genre = genre_service.update_genre(
            genre_id=genre_id,
            name=name,
            description=description,
        )
        if updated_genre:
            st.success(f"Genre '{name}' updated successfully!")
            st.rerun()
        else:
            st.error("Failed to update genre. "
                     "Check your input or session state.")


@st.dialog("Delete Genre")
def delete_genre(genre_id):
    genre_service = GenreService()
    genre = genre_service.get_genre(genre_id=genre_id)

    if not genre:
        st.error("Genre not found or unauthorized access.")
        return

    st.subheader(f"Delete Genre: {genre['name']}")
    if st.button("Confirm Delete"):
        genre_service.delete_genre(genre_id)
        st.success(f"Genre '{genre['name']}' deleted successfully!")
        st.rerun()

    if not genre:
        st.error("Failed to delete genre. "
                 "Check your input or session state.")
        return
