import streamlit as st
from dotenv import load_dotenv
from actors.page import show_actors
from stats.page import show_stats
from genres.page import show_genres
from login.page import show_login
from movies.page import show_movies
from reviews.page import show_reviews


load_dotenv()


def main():
    if "token" not in st.session_state:
        show_login()
    else:
        st.title("Flix App")

        menu_option = st.sidebar.selectbox(
            "Menu",
            [
                "Home",
                "Stats",
                "Actors",
                "Genres",
                "Movies",
                "Reviews",
                "About",
                "Contact",
            ],
        )

        if menu_option == "Home":
            st.header(
                "Welcome to Flix App! A Movie Recommendation System"
            )
            st.subheader(
                "This app recommends movies based on your preferences."
            )

        elif menu_option == "Stats":
            show_stats()

        elif menu_option == "Actors":
            show_actors()

        elif menu_option == "Genres":
            show_genres()

        elif menu_option == "Movies":
            show_movies()

        elif menu_option == "Reviews":
            show_reviews()

        elif menu_option == "About":
            st.header("Welcome to the About Section")
            st.subheader("Learn more about this app.")

        elif menu_option == "Contact":
            st.header("Welcome to the Contact Section")
            st.subheader("Get in touch with us.")


if __name__ == "__main__":
    main()
