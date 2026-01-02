import pytest
from unittest.mock import Mock, patch
from movies.service import MovieService


@pytest.fixture
def mock_movie_repo():
    return Mock()


@pytest.fixture
def movie_service(mock_movie_repo):
    with patch("movies.service.MovieRepository", return_value=mock_movie_repo):
        service = MovieService()
        return service


class TestMovieService:
    def test_get_movies_caching(self, movie_service, mock_streamlit):
        mock_streamlit.session_state.update(
            {"movies": [{"id": 1, "title": "Cached"}]}
        )
        result = movie_service.get_movies()
        assert result == [{"id": 1, "title": "Cached"}]
        movie_service.repository.get_movies.assert_not_called()

    def test_create_movie_defaults(self, movie_service, mock_streamlit):
        mock_streamlit.session_state.update({"movies": []})
        movie_service.repository.create_movie.return_value = {
            "id": 1,
            "title": "New",
            "actors": [],
        }

        movie_service.create_movie(
            title="New",
            genre="Action",
            description=None,
            release_date="2023-01-01",
            duration=120,
        )

        # Verify actors defaulted to []
        call_args = movie_service.repository.create_movie.call_args[0][0]
        assert call_args["actors"] == []
        assert call_args["description"] == ""

    def test_get_movies_stats(self, movie_service):
        movie_service.repository.get_movies_stats.return_value = {"count": 10}
        result = movie_service.get_movies_stats()
        assert result == {"count": 10}
