import pandas as pd
from unittest.mock import patch

from src.extract.spotify_extract import get_user_data, get_artist_data, get_album_data, get_track_data

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
        assert len(result.columns) == 4

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
        assert len(result.columns) == 4


def test_get_album_data():

    mock_album_data = {
    "album_type": "album",
    "total_tracks": 12,
    "available_markets": ["GB", "US"],
    "external_urls": {
        "spotify": "https://open.spotify.com/album/test123"
    },
    "href": "https://api.spotify.com/v1/albums/test123",
    "id": "test123",
    "images": [
        {
            "height": 640,
            "url": "https://i.scdn.co/image/test",
            "width": 640
        }
    ],
    "name": "Test Album",
    "release_date": "2025-09-26",
    "release_date_precision": "day",
    "type": "album",
    "uri": "spotify:album:test123",
    "artists": [
        {
            "external_urls": {
                "spotify": "https://open.spotify.com/artist/artist123"
            },
            "href": "https://api.spotify.com/v1/artists/artist123",
            "id": "artist123",
            "name": "Test Artist",
            "type": "artist",
            "uri": "spotify:artist:artist123"
        }
    ],
    "tracks": {
        "href": "https://api.spotify.com/v1/albums/test123/tracks",
        "limit": 20,
        "next": None,
        "offset": 0,
        "previous": None,
        "total": 12,
        "items": []
    },
    "copyrights": [],
    "external_ids": {
        "upc": "123456789012"
    },
    "genres": [],
    "label": "Test Records",
    "popularity": 65
    }

    with patch("src.extract.spotify_extract.sp.album") as mock_spotify:
        mock_spotify.return_value = mock_album_data.copy()
    
        result = get_album_data('id123')
    
        mock_spotify.assert_called_once_with(album_id="id123")
            
        assert isinstance(result, pd.DataFrame)
        
        assert "album_type" in result.columns
        assert "total_tracks" in result.columns
        assert "available_markets" in result.columns
        assert "uri" in result.columns
        assert "name" in result.columns
        assert "release_date" in result.columns
        assert "release_date_precision" in result.columns
        assert "id" in result.columns
        assert "type" in result.columns
        assert "genres" in result.columns
        assert "label" in result.columns
        assert "popularity" in result.columns
            
        assert "external_urls" not in result.columns
        assert "href" not in result.columns
        assert "images" not in result.columns
        assert "artists" not in result.columns
        assert "tracks" not in result.columns
        assert "copyrights" not in result.columns
        assert "external_ids" not in result.columns
    
        assert len(result) == 1
        assert len(result.columns) == 12


def test_get_track_data():

    mock_track_data = {
        "id": "track123",
        "name": "Test Track",
        "uri": "spotify:track:track123",
        "artists": [],
        "external_ids": {},
        "external_urls": {},
        "href": "https://api.spotify.com",
        "album": {
            "uri": "spotify:album:album123"
        }
    }

    with patch("src.extract.spotify_extract.sp.track") as mock_spotify:
            mock_spotify.return_value = mock_track_data.copy()
        
            result = get_track_data('id123')
        
            mock_spotify.assert_called_once_with(track_id="id123")
                
            assert isinstance(result, pd.DataFrame)
            
            assert "id" in result.columns
            assert "name" in result.columns
            assert "uri" in result.columns
            assert "album_uri" in result.columns

            assert "external_urls" not in result.columns
            assert "href" not in result.columns
            assert "external_ids" not in result.columns
            assert "artists" not in result.columns

            assert len(result) == 1
            assert len(result.columns) == 4