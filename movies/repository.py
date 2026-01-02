import requests
import streamlit as st
from login.service import logout


class MovieRepository:
    def __init__(self):
        self.__base_url = "https://callmenate.pythonanywhere.com/api/v1/"
        self.__auth_url = f"{self.__base_url}movies/"
        self.__headers = {"Authorization": f"Bearer {st.session_state.token}"}

    def get_movies(self):
        response = requests.get(self.__auth_url, headers=self.__headers)

        if response.status_code == 200:
            return response.json()
        if response.status_code == 401:
            st.error("Unauthorized access. Please log in again.")
            logout()
            return None
        raise Exception(
            "Failed to fetch movies. "
            f"Status code: {response.status_code}, "
            f"Response: {response.text}"
        )

    def get_movie(self, movie_id):
        response = requests.get(
            f"{self.__auth_url}{movie_id}/",
            headers=self.__headers
        )

        if response.status_code == 200:
            return response.json()
        if response.status_code == 401:
            st.error("Unauthorized access. Please log in again.")
            logout()
            return None
        raise Exception(
            "Failed to fetch movie. "
            f"Status code: {response.status_code}, "
            f"Response: {response.text}"
        )

    def create_movie(self, movie):
        response = requests.post(
            self.__auth_url,
            headers=self.__headers,
            data=movie,
        )

        if response.status_code == 201:
            return response.json()
        if response.status_code == 401:
            st.error("Unauthorized access. Please log in again.")
            logout()
            return None
        raise Exception(
            "Failed to create movie."
            f" Status code: {response.status_code}, "
            f"Response: {response.json().get('name', response.text)}"
        )

    def update_movie(self, movie_id, movie, method="put"):
        url = f"{self.__auth_url}{movie_id}/"
        if method.lower() == "patch":
            response = requests.patch(
                url=url,
                headers=self.__headers,
                data=movie,
            )
        else:
            response = requests.put(
                url=url,
                headers=self.__headers,
                data=movie,
            )

        if response.status_code in [200, 201]:
            return response.json()
        if response.status_code == 401:
            st.error("Unauthorized access. Please log in again.")
            logout()
            return None
        raise Exception(
            "Failed to update movie. "
            f"Status code: {response.status_code}, "
            f"Response: {response.json().get('name', response.text)}"
        )

    def delete_movie(self, movie_id):
        response = requests.delete(
            f"{self.__auth_url}{movie_id}/",
            headers=self.__headers
        )

        if response.status_code == 204:
            return True
        if response.status_code == 401:
            st.error("Unauthorized access. Please log in again.")
            logout()
            return False
        raise Exception(
            "Failed to update movie. "
            f"Status code: {response.status_code}, "
            f"Response: {response.json().get('name', response.text)}"
        )

    def get_movies_stats(self):
        response = requests.get(
            f"{self.__base_url}movies/stats/",
            headers=self.__headers
        )

        if response.status_code == 200:
            return response.json()
        if response.status_code == 401:
            st.error("Unauthorized access. Please log in again.")
            logout()
            return None
        raise Exception(
            "Failed to fetch movie stats. "
            f"Status code: {response.status_code}, "
            f"Response: {response.text}"
        )
