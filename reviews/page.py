import streamlit as st
import pandas as pd
from reviews.service import ReviewService
from movies.service import MovieService


def show_reviews():
    review_service = ReviewService()
    reviews = review_service.get_reviews()
    df_reviews = pd.DataFrame(reviews)

    if not reviews:
        st.warning("No reviews found or unauthorized access.")
        st.button(
            "Create Review",
            on_click=create_review,
            key="create_review"
        )
        return
    else:
        st.header("Welcome to the List of Reviews")
        df_reviews = pd.json_normalize(reviews)

        st.button(
            "Create Review",
            on_click=create_review,
            key="create_review"
        )

        for _, review in df_reviews.iterrows():
            movie = MovieService().get_movie(movie_id=review['movie'])

            tile = st.container(border=True)
            tile.markdown(f"### Review for: {movie['title']}")
            tile.markdown(f"**Rating:** {review['rating']}")
            tile.markdown(f"**Comment:** {review['comment']}")

            review_delete = tile.empty()
            review_delete.button(
                "Delete",
                on_click=delete_review,
                args=(review['id'],),
                key=f"delete_{review['id']}"
            )


@st.dialog("Create Review")
def create_review():
    review_service = ReviewService()
    movie_service = MovieService()
    movies = movie_service.get_movies()
    if not movies:
        st.warning("No movies available to review.")
        return

    movie_options = {movie['title']: movie['id'] for movie in movies}
    selected_movie = st.selectbox(
        "Select Movie",
        options=list(movie_options.keys())
    )

    rating = st.slider("Rating", min_value=1, max_value=5, value=3)
    comment = st.text_area("Comment")

    if st.button("Submit Review"):
        new_review = review_service.create_review(
            movie=movie_options[selected_movie],
            rating=rating,
            comment=comment
        )
        if new_review:
            st.success("Review created successfully!")
            st.rerun()
        else:
            st.error("Failed to create review.")


@st.dialog("Delete Review")
def delete_review(review_id):
    review_service = ReviewService()
    if review_service.delete_review(review_id):
        st.success("Review deleted successfully!")
        st.rerun()
    else:
        st.error("Failed to delete review.")
