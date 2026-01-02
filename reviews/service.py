import streamlit as st
from reviews.repository import ReviewRepository


class ReviewService:

    def __init__(self):
        self.__repository = ReviewRepository()

    def get_reviews(self):
        if 'reviews' in st.session_state:
            return st.session_state.reviews
        reviews = self.__repository.get_reviews()
        st.session_state.reviews = reviews
        return reviews

    def create_review(self, movie, rating, comment):
        review = {
            "movie": movie,
            "rating": rating,
            "comment": comment
        }

        new_review = self.__repository.create_review(review)
        st.session_state.reviews.append(new_review)
        return new_review

    def delete_review(self, review_id):
        return self.__repository.delete_review(review_id)
