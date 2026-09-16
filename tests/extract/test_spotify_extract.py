import pandas as pd
from unittest.mock import patch

from src.extract.spotify_extract import get_user_data, get_artist_data

def test_get_user_data():

    mock_user_data = {
        "display_name": "Test User",
        "id": "test123",
        "email": "test@example.com",
        "followers": {"total": 42},
        "explicit_content": {"filter_enabled": False},
        "external_urls": {"spotify": "https://spotify.com"},
        "href": "https://api.spotify.com",
        "images": []
    }

    with patch("src.extract.spotify_extract.sp.current_user") as mock_spotify:
        mock_spotify.return_value = mock_user_data.copy()

        result = get_user_data()

        mock_spotify.assert_called_once()

        assert isinstance(result, pd.DataFrame)

        assert "display_name" in result.columns
        assert "id" in result.columns
        assert "email" in result.columns

        assert "explicit_content" not in result.columns
        assert "external_urls" not in result.columns
        assert "href" not in result.columns
        assert "images" not in result.columns

        assert len(result) == 1

def test_get_artist_data():

    mock_artist_data = {
        "id": "artist123",
        "name": "Test Artist",
        "type": "artist",
        "uri": "spotify:artist:artist123",
        "external_urls": {"spotify": "https://spotify.com"},
        "href": "https://api.spotify.com",
        "images": []
    }

    with patch("src.extract.spotify_extract.sp.artist") as mock_spotify:
        mock_spotify.return_value = mock_artist_data.copy()

        result = get_artist_data('id123')

        mock_spotify.assert_called_once_with(artist_id="id123")
        
        assert isinstance(result, pd.DataFrame)
        
        assert "id" in result.columns
        assert "name" in result.columns
        assert "type" in result.columns
        assert "uri" in result.columns
        
        assert "external_urls" not in result.columns
        assert "href" not in result.columns
        assert "images" not in result.columns

        assert len(result) == 1
