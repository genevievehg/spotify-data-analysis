import duckdb

def retrieve_top_songs(df, n=5):

    data = df

    query = f"""WITH song_count AS(
    SELECT master_metadata_track_name, 
    spotify_track_uri,
    COUNT(spotify_track_uri) AS play_count
    FROM data
    GROUP BY master_metadata_track_name, spotify_track_uri
    )
    SELECT *
    FROM song_count
    WHERE play_count >={n}
    ORDER BY play_count DESC;
    """

    top_songs = duckdb.sql(query)


    return top_songs.df()

def retrieve_top_artists(df, n=50):

    data = df

    query = f"""WITH artist_count AS (
    SELECT master_metadata_album_artist_name,
    COUNT(master_metadata_album_artist_name) AS play_count
    FROM data
    GROUP BY master_metadata_album_artist_name
    )
    SELECT *
    FROM artist_count
    WHERE play_count >={n}
    ORDER by play_count DESC;
    """

    artist_play_count = duckdb.sql(query)

    return artist_play_count.df()


def retrieve_top_albums(df, n=25):

    data = df

    query = f"""WITH album_play_count AS (
    SELECT master_metadata_album_album_name,
    COUNT(master_metadata_album_album_name) AS play_count
    FROM data
    GROUP BY master_metadata_album_album_name
    )
    SELECT *
    FROM album_play_count
    WHERE play_count >={n}
    ORDER by play_count DESC;
    """

    album_play_count = duckdb.sql(query)

    return album_play_count.df()