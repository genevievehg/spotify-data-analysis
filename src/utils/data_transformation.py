import pandas as pd

from pathlib import Path


def get_list_of_dataframes_in_folder(path):
    
    folder = Path(path)

    files = [f for f in folder.iterdir() if f.is_file()]

    df_list = []
    for file in files:
        df = pd.read_parquet(file)
        df_list.append(df)

    return df_list