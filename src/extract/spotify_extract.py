import logging
import os
import time

import numpy as np
import pandas as pd
from pathlib import Path
from spotipy.exceptions import SpotifyException

from src.extract.spotify_client import spotify_client


Path("logs").mkdir(exist_ok=True)

logger = logging.getLogger("SimpleLogger")

logging.basicConfig(
    filename="logs/spotify_extract.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG
    )


sp = spotify_client()


def get_user_data():

    result = sp.current_user()
    dictionary_keys = result.keys()

    keys_to_remove = ['explicit_content', 'external_urls', 'href', 'images']

    for key in keys_to_remove:
        if key in dictionary_keys:
            del result[key]

    if 'followers' in result.keys():
        result['followers'] = result['followers']['total']
    
    df = pd.DataFrame(result, index=[0])

    return df


def get_artist_data(id: str):
    
    result = sp.artist(artist_id=id)
    dictionary_keys = result.keys()

    keys_to_remove = ['external_urls', 'href', 'images']

    for key in keys_to_remove:
        if key in dictionary_keys:
            del result[key]
    
    df = pd.DataFrame(result, index=[0])

    return df
    

def get_album_data(id: str):

    result = sp.album(album_id=id)
    dictionary_keys = result.keys()

    keys_to_remove = ['external_urls', 'href', 'images', 'artists', 'tracks', 'copyrights', 'external_ids']

    for key in keys_to_remove:
        if key in dictionary_keys:
            del result[key]

    df = pd.DataFrame([result], index=[0])
    return df


def get_track_data(id: str):

    result = sp.track(track_id=id)
    dictionary_keys = result.keys()

    keys_to_remove = ['external_ids', 'external_urls', 'href']

    for key in keys_to_remove:
        if key in dictionary_keys:
            del result[key]

    if 'album' in result.keys():
        result['album_uri'] = result['album']['uri']
        del result['album']

    if 'artists' in result.keys():
        result['artist_uris'] = [artist["uri"] for artist in result["artists"]]
        del result['artist']

    df = pd.DataFrame(result, index=[0])

    return df

#test = get_track_data('0vMctOnb4YNIvbqgkbWNDy')
#print(test)


def get_multiple_track_data(unique_track_uris: np.ndarray):
    
    cached_metadata_path = 'data/raw/spotify_api/cached_track_metadata.parquet'

    if os.path.isfile(cached_metadata_path):
        metadata_df = pd.read_parquet(cached_metadata_path)
        existing_track_uris = set(metadata_df["uri"])
        track_uris_to_enrich = set(unique_track_uris) - existing_track_uris

    else:
        metadata_df = pd.DataFrame()
        track_uris_to_enrich = unique_track_uris


    logger.info(f'{len(track_uris_to_enrich)} tracks to enrich')

    tracks = []

    for i, track_uri in enumerate(track_uris_to_enrich, start=1):

        try:
            track_df = get_track_data(track_uri)
        except SpotifyException as e:
            if e.http_status == 429:
                logger.warning(
                    f'Spotify rate limit reached after {i-1} tracks. '
                    'Stopping enrichment.')
                break
            raise

        track_df['uri'] = track_uri
        tracks.append(track_df)

        time.sleep(1)

        if i % 50 == 0 and tracks:
            new_metadata_df = pd.concat(tracks)
            metadata_df = pd.concat([metadata_df, new_metadata_df], ignore_index=True)
            metadata_df.to_parquet(cached_metadata_path)
            tracks = []

    if tracks:
        new_metadata_df = pd.concat(tracks)
        metadata_df = pd.concat([metadata_df, new_metadata_df], ignore_index=True)
        metadata_df.to_parquet(cached_metadata_path)

    return metadata_df