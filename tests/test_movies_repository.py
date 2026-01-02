import pytest
from unittest.mock import Mock, patch
from movies.repository import MovieRepository


@pytest.fixture
def movie_repository(mock_auth_token):
    return MovieRepository()


class TestMovieRepository:
    @patch("movies.repository.requests")
    def test_get_movies_success(self, mock_requests, movie_repository):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1, "title": "Movie 1"}]
        mock_requests.get.return_value = mock_response

        result = movie_repository.get_movies()
        assert result == [{"id": 1, "title": "Movie 1"}]

    @patch("movies.repository.requests")
    def test_create_movie_success(self, mock_requests, movie_repository):
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": 1, "title": "New Movie"}
        mock_requests.post.return_value = mock_response

        movie_data = {"title": "New Movie"}
        result = movie_repository.create_movie(movie_data)
        assert result == {"id": 1, "title": "New Movie"}

    @patch("movies.repository.requests")
    def test_get_movies_stats_success(self, mock_requests, movie_repository):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"total_movies": 100}
        mock_requests.get.return_value = mock_response

        result = movie_repository.get_movies_stats()
        assert result == {"total_movies": 100}
