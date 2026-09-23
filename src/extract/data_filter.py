import duckdb

def retrieve_top_songs(df, n=5):

    data = df

    query = f"""
    SELECT master_metadata_track_name, 
    spotify_track_uri,
    COUNT(spotify_track_uri) AS play_count
    FROM data
    GROUP BY master_metadata_track_name, spotify_track_uri
    ORDER by play_count DESC;
    """

    song_count = duckdb.sql(query)

    song_count.write_parquet("data/raw/reference/song_plays.parquet")

    query_2 = f"""
    SELECT *
    FROM song_count
    WHERE play_count >={n};
    """

    result = duckdb.sql(query_2)

    return result

def retrieve_top_artists(df, n=50):

    data = df

    query = f"""
    SELECT master_metadata_album_artist_name,
    COUNT(master_metadata_album_artist_name) AS play_count
    FROM data
    GROUP BY master_metadata_album_artist_name
    ORDER by play_count DESC;
    """

    artist_play_count = duckdb.sql(query)

    artist_play_count.write_parquet("data/raw/reference/artist_plays.parquet")

    query_2 = f"""
    SELECT *
    FROM artist_play_count
    WHERE play_count >={n};
    """

    result = duckdb.sql(query_2)

    return result


def retrieve_top_albums(df, n=25):

    data = df

    query = f"""
    SELECT master_metadata_album_album_name,
    COUNT(master_metadata_album_album_name) AS play_count
    FROM data
    GROUP BY master_metadata_album_album_name
    ORDER by play_count DESC;
    """

    album_play_count = duckdb.sql(query)

    album_play_count.write_parquet("data/raw/reference/album_plays.parquet")

    query_2 = f"""
    SELECT *
    FROM album_play_count
    WHERE play_count >={n};
    """

    result = duckdb.sql(query_2)

    return result