import pytest
from unittest.mock import Mock, patch
from genres.service import GenreService


@pytest.fixture
def mock_repository():
    return Mock()


@pytest.fixture
def genre_service(mock_repository):
    with patch("genres.service.GenreRepository", return_value=mock_repository):
        service = GenreService()
        return service


class TestGenreService:
    def test_get_genres_from_session_cache(
        self, genre_service, mock_streamlit
    ):
        # Arrange
        mock_streamlit.session_state.update(
            {"genres": [{"id": 1, "name": "Cached"}]}
        )

        # Act
        result = genre_service.get_genres()

        # Assert
        assert result == [{"id": 1, "name": "Cached"}]
        # Repository should NOT be called
        genre_service._GenreService__repository.get_genres.assert_not_called()

    def test_get_genres_fetch_from_repo(
        self, genre_service, mock_streamlit
    ):
        # Arrange
        mock_streamlit.session_state.clear()  # Empty cache
        expected_genres = [{"id": 2, "name": "Fetched"}]
        genre_service._GenreService__repository.get_genres.return_value = (
            expected_genres
        )

        # Act
        result = genre_service.get_genres()

        # Assert
        assert result == expected_genres
        assert mock_streamlit.session_state["genres"] == expected_genres
        genre_service._GenreService__repository.get_genres.assert_called_once()

    def test_create_genre(self, genre_service, mock_streamlit):
        # Arrange
        mock_streamlit.session_state.update({"genres": []})
        new_genre = {"id": 3, "name": "New Genre"}
        genre_service._GenreService__repository.create_genre.return_value = new_genre

        # Act
        result = genre_service.create_genre("New Genre")

        # Assert
        assert result == new_genre
        assert new_genre in mock_streamlit.session_state["genres"]
        genre_service._GenreService__repository.create_genre.assert_called_once()

    def test_update_genre(self, genre_service):
        # Arrange
        updated_genre = {"id": 1, "name": "Updated"}
        genre_service._GenreService__repository.update_genre.return_value = (
            updated_genre
        )

        # Act
        result = genre_service.update_genre(1, "Updated")

        # Assert
        assert result == updated_genre
        genre_service._GenreService__repository.update_genre.assert_called_once()
