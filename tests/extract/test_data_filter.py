from src.extract.data_filter import retrieve_top_songs, retrieve_top_artists, retrieve_top_albums

import pandas as pd

test_raw_df = pd.DataFrame({
    "ts": [
        "2018-01-02T09:52:56Z",
        "2018-01-02T10:15:22Z",
        "2018-01-03T14:32:10Z",
        "2018-01-04T18:45:33Z",
        "2018-01-05T20:12:01Z",
        "2018-01-06T21:30:44Z",
        "2018-01-07T08:15:12Z",
        "2018-01-08T12:42:55Z",
        "2018-01-09T16:20:30Z",
        "2018-01-10T19:05:17Z",
    ],
    "platform": [
        "ios",
        "ios",
        "android",
        "ios",
        "web_player",
        "ios",
        "android",
        "ios",
        "ios",
        "web_player",
    ],
    "ms_played": [
        210000,
        180000,
        240000,
        220000,
        195000,
        230000,
        205000,
        190000,
        250000,
        175000,
    ],
    "conn_country": [
        "GB",
        "GB",
        "GB",
        "GB",
        "GB",
        "GB",
        "GB",
        "GB",
        "GB",
        "GB",
    ],
    "ip_addr": [
        "192.168.1.1",
        "192.168.1.1",
        "192.168.1.2",
        "192.168.1.1",
        "192.168.1.3",
        "192.168.1.1",
        "192.168.1.2",
        "192.168.1.1",
        "192.168.1.3",
        "192.168.1.1",
    ],
    "spotify_track_uri": [
        "spotify:track:track_1",
        "spotify:track:track_1",
        "spotify:track:track_2",
        "spotify:track:track_1",
        "spotify:track:track_3",
        "spotify:track:track_2",
        "spotify:track:track_1",
        "spotify:track:track_3",
        "spotify:track:track_2",
        "spotify:track:track_4",
    ],
    "master_metadata_track_name": [
        "Track One",
        "Track One",
        "Track Two",
        "Track One",
        "Track Three",
        "Track Two",
        "Track One",
        "Track Three",
        "Track Two",
        "Track Four",
    ],
    "master_metadata_album_artist_name": [
        "Artist A",
        "Artist A",
        "Artist B",
        "Artist A",
        "Artist A",
        "Artist B",
        "Artist A",
        "Artist A",
        "Artist B",
        "Artist C",
    ],
    "master_metadata_album_album_name": [
        "Album A",
        "Album A",
        "Album B",
        "Album A",
        "Album C",
        "Album B",
        "Album A",
        "Album C",
        "Album B",
        "Album D",
    ],
    "reason_start": [
        "trackdone",
        "trackdone",
        "trackdone",
        "trackdone",
        "trackdone",
        "trackdone",
        "trackdone",
        "trackdone",
        "trackdone",
        "trackdone",
    ],
    "reason_end": [
        "trackdone",
        "trackdone",
        "trackdone",
        "trackdone",
        "trackdone",
        "trackdone",
        "trackdone",
        "trackdone",
        "trackdone",
        "trackdone",
    ],
    "shuffle": [
        False, False, True, False, True,
        False, True, False, True, False
    ],
    "skipped": [
        False, False, False, False, True,
        False, False, True, False, False
    ],
    "offline": [
        False, False, False, True, False,
        False, False, False, True, False
    ],
    "incognito_mode": [
        False, False, False, False, False,
        False, False, False, False, False
    ],
})

def test_retrieve_top_songs_returns_df():

    result = retrieve_top_songs(test_raw_df)

    assert isinstance(result, pd.DataFrame)


def test_retrieve_top_artists_returns_df():

    result = retrieve_top_artists(test_raw_df)

    assert isinstance(result, pd.DataFrame)


def test_retrieve_top_albums_returns_df():

    result = retrieve_top_albums(test_raw_df)

    assert isinstance(result, pd.DataFrame)