import pandas as pd
import streamlit as st
from datetime import datetime
# from st_aggrid import AgGrid
from actors.service import ActorService

nationalities = [
    'AUSTRALIA',
    'BRAZIL',
    'CANADA',
    'CHINA',
    'FRANCE',
    'GERMANY',
    'INDIA',
    'ITALY',
    'UK',
    'USA',
    'OTHER',
]


def show_actors():
    actor_service = ActorService()
    actors = actor_service.get_actors()

    if not actors:
        st.warning("No actors found or unauthorized access.")
        st.button(
            "Create Actor",
            on_click=create_actor,
            key="create_actor"
        )
        return
    else:
        st.header("Welcome to the List of Actors")
        df_actors = pd.json_normalize(actors)

        st.button(
            "Create Actor",
            on_click=create_actor,
            key="create_actor"
        )

        for _, actor in df_actors.iterrows():
            tile = st.container(border=True)
            tile.markdown(f"### {actor['name']}")
            tile.markdown(
                f"**Date of Birth:** {actor.get('date_of_birth', 'N/A')}"
            )
            tile.markdown(
                f"**Nationality:** {actor.get('nationality', 'N/A')}"
            )
            tile.markdown(
                f"**Biography:** {actor.get('biography', 'N/A')}"
            )
            actor_update, actor_delete = tile.columns(2, gap=None)
            actor_update.button(
                "Edit",
                on_click=update_actor,
                args=(actor['id'],),
                key=f"edit_{actor['id']}"
            )
            actor_delete.button(
                "Delete",
                on_click=delete_actor,
                args=(actor['id'],),
                key=f"delete_{actor['id']}"
            )


@st.dialog("Create Actor")
def create_actor():
    actor_service = ActorService()
    st.subheader("Submit new Actor")
    name = st.text_input("Actor Name")
    date_of_birth = st.date_input(
        label="Date of Birth",
        value=datetime.today(),
        min_value=datetime(1900, 1, 1),
        max_value=datetime.today(),
        format="DD/MM/YYYY"
    )
    nationality = st.selectbox(
        label="Nationality",
        options=nationalities
    )
    biography = st.text_area("Biography")

    if st.button("Submit"):
        new_actor = actor_service.create_actor(
            name=name,
            date_of_birth=date_of_birth,
            nationality=nationality,
            biography=biography,
        )
        if new_actor:
            st.success(f"Actor '{name}' added successfully!")
            st.rerun()
        else:
            st.error("Failed to add actor. Please try again.")


@st.dialog("Update Actor")
def update_actor(actor_id):
    actor_service = ActorService()
    actor = actor_service.get_actor(actor_id=actor_id)

    if not actor:
        st.error("Actor not found or unauthorized access.")
        return

    st.subheader(f"Update Actor: {actor['name']}")
    name = st.text_input("Actor Name", value=actor['name'])
    date_of_birth = st.date_input(
        label="Date of Birth",
        value=datetime.today(),
        min_value=datetime(1900, 1, 1),
        max_value=datetime.today(),
        format="DD/MM/YYYY"
    )
    nationality = st.selectbox(
        label="Nationality",
        options=nationalities,
        index=nationalities.index(actor.get('nationality', ''))
    )
    biography = st.text_area(
        "Biography",
        value=actor.get('biography', '')
    )
    if st.button("Update"):
        updated_actor = actor_service.update_actor(
            actor_id=actor_id,
            name=name,
            date_of_birth=date_of_birth,
            nationality=nationality,
            biography=biography,
        )
        if updated_actor:
            st.success(f"Actor '{name}' updated successfully!")
            st.rerun()
        else:
            st.error("Failed to update actor. "
                     "Check your input or session state.")


@st.dialog("Delete Actor")
def delete_actor(actor_id):
    actor_service = ActorService()
    actor = actor_service.get_actor(actor_id=actor_id)

    if not actor:
        st.error("Actor not found or unauthorized access.")
        return

    st.subheader(f"Delete Actor: {actor['name']}")
    if st.button("Confirm Delete"):
        st.success(f"Actor '{actor['name']}' deleted successfully!")
        st.rerun()
    else:
        st.error("Failed to delete actor. "
                 "Check your input or session state.")
        return
