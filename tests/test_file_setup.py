from file_setup import convert_json_to_parquet
import pandas as pd

def test_convert_json_to_parquet_converts_files_sucessfully(tmp_path):
    input_path = tmp_path / 'test.json'
    output_path = tmp_path / 'test.parquet'

    test_data = pd.DataFrame({
        "song": ["Happy", "Love Forever"],
        "artist": ["Prince", "Cher"]
        })
    
    test_data.to_json(input_path, orient="records")

    convert_json_to_parquet(str(input_path), str(output_path))

    assert output_path.exists()    