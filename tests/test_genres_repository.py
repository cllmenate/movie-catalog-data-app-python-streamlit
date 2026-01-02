import pytest
from unittest.mock import Mock, patch
from genres.repository import GenreRepository


@pytest.fixture
def genre_repository(mock_auth_token):
    return GenreRepository()


class TestGenreRepository:
    @patch("genres.repository.requests")
    def test_get_genres_success(self, mock_requests, genre_repository):
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": 1, "name": "Action"}]
        mock_requests.get.return_value = mock_response

        # Act
        result = genre_repository.get_genres()

        # Assert
        assert result == [{"id": 1, "name": "Action"}]
        mock_requests.get.assert_called_once()

    @patch("genres.repository.requests")
    def test_get_genres_unauthorized(self, mock_requests, genre_repository):
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 401
        mock_requests.get.return_value = mock_response

        with patch("genres.repository.logout") as mock_logout:
            # Act
            result = genre_repository.get_genres()

            # Assert
            assert result is None
            mock_logout.assert_called_once()

    @patch("genres.repository.requests")
    def test_create_genre_success(self, mock_requests, genre_repository):
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": 1, "name": "Drama"}
        mock_requests.post.return_value = mock_response

        genre_data = {"name": "Drama"}

        # Act
        result = genre_repository.create_genre(genre_data)

        # Assert
        assert result == {"id": 1, "name": "Drama"}
        mock_requests.post.assert_called_once()

    @patch("genres.repository.requests")
    def test_delete_genre_success(self, mock_requests, genre_repository):
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 204
        mock_requests.delete.return_value = mock_response

        # Act
        result = genre_repository.delete_genre(1)

        # Assert
        assert result is True
        mock_requests.delete.assert_called_once()
