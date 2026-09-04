from file_setup import convert_json_to_parquet, convert_files_in_folder
import pandas as pd
import pytest
import os

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


def test_convert_json_to_parquet_handles_missing_input_directory(tmp_path):
    output_path = tmp_path / 'test.parquet'

    with pytest.raises(FileNotFoundError) as e:
        convert_json_to_parquet('non_existent_file_path', output_path)

    assert e.value.args[0] == 'File non_existent_file_path not found. Please enter valid location'


def test_convert_json_to_parquet_handles_missing_output_directory(tmp_path):
    input_path = tmp_path / 'test.json'
    output_path = tmp_path / "missing" / "output.parquet"

    test_data = pd.DataFrame({
            "song": ["Happy", "Love Forever"],
            "artist": ["Prince", "Cher"]
            })
        
    test_data.to_json(input_path, orient="records")

    with pytest.raises(FileNotFoundError) as e:
        convert_json_to_parquet(str(input_path), str(output_path))

    assert e.value.args[0] == f'Cannot write {output_path}. Directory does not exist'


def test_convert_files_in_folder(tmp_path):
    input_directory = tmp_path / 'test_input'
    input_directory.mkdir()
    output_directory = tmp_path / 'test_output'
    output_directory.mkdir()

    json_files = [{
            "song": ["Happy", "Love Forever"],
            "artist": ["Prince", "Cher"]},
            {"song": ["Happy", "Love Forever"],
            "artist": ["Prince", "Cher"]
            }]

    for i, file in enumerate(json_files):
        df = pd.DataFrame(file)
        df.to_json(input_directory / f'test_input_{i}.json', orient="records")

    convert_files_in_folder(str(input_directory), str(output_directory))

    assert (output_directory / 'test_input_0.parquet').exists()
    assert (output_directory / 'test_input_1.parquet').exists()


def test_convert_files_in_folder_handles_missing_input_directory(tmp_path):
    input_directory = tmp_path / 'test_input'
    output_directory = tmp_path / 'test_output'

    with pytest.raises(FileNotFoundError) as e:
        convert_files_in_folder(str(input_directory), str(output_directory))

    assert e.value.args[0] == f'{input_directory} does not exist'


def test_convert_files_in_folder_handles_empty_input_directory(tmp_path):
    input_directory = tmp_path / 'test_input'
    input_directory.mkdir()
    output_directory = tmp_path / 'test_output'

    with pytest.raises(FileNotFoundError) as e:
        convert_files_in_folder(str(input_directory), str(output_directory))

    assert e.value.args[0] == f'Input directory is empty'