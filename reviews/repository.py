import requests
import streamlit as st
from login.service import logout


class ReviewRepository:
    def __init__(self):
        self.__base_url = "https://callmenate.pythonanywhere.com/api/v1/"
        self.__auth_url = f"{self.__base_url}reviews/"
        self.__headers = {"Authorization": f"Bearer {st.session_state.token}"}

    def get_reviews(self):
        response = requests.get(self.__auth_url, headers=self.__headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            st.error("Unauthorized access. Please log in again.")
            logout()
        return None
        raise Exception(
            "Failed to fetch reviews. "
            f"Status code: {response.status_code}, "
            f"Response: {response.text}"
        )

    def create_review(self, review):
        response = requests.post(
            self.__auth_url,
            headers=self.__headers,
            json=review,
        )

        if response.status_code == 201:
            return response.json()
        elif response.status_code == 401:
            st.error("Unauthorized access. Please log in again.")
            logout()
        return None
        raise Exception(
            "Failed to create review. "
            f"Status code: {response.status_code}, "
            f"Response: {response.text}"
        )

    def delete_review(self, review_id):
        response = requests.delete(
            f"{self.__auth_url}{review_id}/", headers=self.__headers
        )

        if response.status_code == 204:
            return True
        elif response.status_code == 401:
            st.error("Unauthorized access. Please log in again.")
            logout()
        return False
        raise Exception(
            "Failed to delete review. "
            f"Status code: {response.status_code}, "
            f"Response: {response.text}"
        )
