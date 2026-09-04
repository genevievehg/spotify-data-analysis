from unittest.mock import Mock
from src.extract import spotify_client as spotify_module

def test_spotify_client(monkeypatch):
    mock_auth_manager = Mock()
    mock_spotify_client = Mock()

    monkeypatch.setattr(
        spotify_module,
        "SpotifyPKCE",
        Mock(return_value=mock_auth_manager)
    )

    monkeypatch.setattr(
        spotify_module.spotipy,
        "Spotify",
        Mock(return_value=mock_spotify_client)
    )

    monkeypatch.setenv("SPOTIFY_CLIENT_ID", "test-client-id")

    result = spotify_module.spotify_client()

    assert result == mock_spotify_client