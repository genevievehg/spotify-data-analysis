import pandas as pd
from src.extract.spotify_client import spotify_client


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