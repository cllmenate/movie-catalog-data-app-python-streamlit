import requests
import streamlit as st
from login.service import logout


class ActorRepository:
    def __init__(self):
        self.__base_url = "https://callmenate.pythonanywhere.com/api/v1/"
        self.__auth_url = f"{self.__base_url}actors/"
        self.__headers = {"Authorization": f"Bearer {st.session_state.token}"}

    def get_actors(self):
        response = requests.get(self.__auth_url, headers=self.__headers)

        if response.status_code == 200:
            return response.json()
        if response.status_code == 401:
            st.error("Unauthorized access. Please log in again.")
            logout()
            return None
        raise Exception(
            "Failed to fetch actors. "
            f"Status code: {response.status_code}, "
            f"Response: {response.text}"
        )

    def get_actor(self, actor_id):
        response = requests.get(
            f"{self.__auth_url}{actor_id}/",
            headers=self.__headers
        )

        if response.status_code == 200:
            return response.json()
        if response.status_code == 401:
            st.error("Unauthorized access. Please log in again.")
            logout()
            return None
        raise Exception(
            "Failed to fetch actor. "
            f"Status code: {response.status_code}, "
            f"Response: {response.text}"
        )

    def create_actor(self, actor):
        response = requests.post(
            self.__auth_url,
            headers=self.__headers,
            data=actor,
        )

        if response.status_code == 201:
            return response.json()
        if response.status_code == 401:
            st.error("Unauthorized access. Please log in again.")
            logout()
            return None
        raise Exception(
            "Failed to create actor."
            f" Status code: {response.status_code}, "
            f"Response: {response.json().get('name', response.text)}"
        )

    def update_actor(self, actor_id, actor, method="put"):
        url = f"{self.__auth_url}{actor_id}/"
        if method.lower() == "patch":
            response = requests.patch(
                url=url,
                headers=self.__headers,
                data=actor,
            )
        else:
            response = requests.put(
                url=url,
                headers=self.__headers,
                data=actor,
            )

        if response.status_code in [200, 201]:
            return response.json()
        if response.status_code == 401:
            st.error("Unauthorized access. Please log in again.")
            logout()
            return None
        raise Exception(
            "Failed to update actor. "
            f"Status code: {response.status_code}, "
            f"Response: {response.json().get('name', response.text)}"
        )

    def delete_actor(self, actor_id):
        response = requests.delete(
            f"{self.__auth_url}{actor_id}/",
            headers=self.__headers
        )

        if response.status_code == 204:
            return True
        if response.status_code == 401:
            st.error("Unauthorized access. Please log in again.")
            logout()
            return False
        raise Exception(
            "Failed to delete actor. "
            f"Status code: {response.status_code}, "
            f"Response: {response.text}"
        )
