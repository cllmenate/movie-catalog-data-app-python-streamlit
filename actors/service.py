import streamlit as st
from actors.repository import ActorRepository


class ActorService:

    def __init__(self):
        self.repository = ActorRepository()

    def get_actors(self):
        if 'actors' in st.session_state:
            return st.session_state.actors
        actors = self.repository.get_actors()
        st.session_state.actors = actors
        return actors

    def get_actor(self, actor_id):
        actor = self.repository.get_actor(actor_id)
        return actor

    def create_actor(self, name, date_of_birth, nationality, biography=None):
        actor = dict(
            name=name,
            date_of_birth=date_of_birth,
            nationality=nationality,
            biography=biography if biography else ""
        )

        new_actor = self.repository.create_actor(actor)
        st.session_state.actors.append(new_actor)
        return new_actor

    def update_actor(
            self,
            actor_id,
            name,
            date_of_birth,
            nationality,
            biography=None,
            method="put"
    ):
        actor = dict(
            name=name,
            date_of_birth=date_of_birth,
            nationality=nationality,
            biography=biography if biography else ""
        )
        update_actor = self.repository.update_actor(actor_id, actor, method)
        if update_actor:
            for i, a in enumerate(st.session_state.actors):
                if a['id'] == actor_id:
                    st.session_state.actors[i] = actor
                    break
        return update_actor

    def delete_actor(self, actor_id):
        return self.repository.delete_actor(actor_id)
