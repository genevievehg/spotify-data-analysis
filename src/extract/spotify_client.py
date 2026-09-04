import os
import spotipy
from spotipy.oauth2 import SpotifyPKCE
from dotenv import load_dotenv

load_dotenv()

def spotify_client():

    auth_manager = SpotifyPKCE(
        client_id=os.environ["SPOTIFY_CLIENT_ID"],
        redirect_uri="http://127.0.0.1:8888/callback",
        scope="user-read-playback-state playlist-read-private playlist-read-collaborative user-read-private user-read-email",
        open_browser=False,
        cache_path=".spotify_cache"
    )

    sp = spotipy.Spotify(auth_manager=auth_manager)

    return sp