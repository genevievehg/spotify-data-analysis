import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def convert_json_to_parquet(input_file_path: str, output_file_path: str):

    df = pd.read_json(input_file_path)

    table = pa.Table.from_pandas(df)

    pq.write_table(table, output_file_path)


def convert_files_in_folder(input_directory: str, output_directory: str):

    file_list = os.scandir(input_directory)

    for file in file_list:
        if file.is_file():
            input_file_path = input_directory + '/' + file.name
            output_file_path = output_directory + '/' + os.path.splitext(file.name)[0] + '.parquet'
            convert_json_to_parquet(input_file_path, output_file_path)
        else:
            pass


def user_interface():
    print('Enter data directory where your files are located')
    input_directory = input()

    try:
        file_list = list(os.scandir(input_directory))
        input_count = 0
        for path in file_list:
            if path.is_file():
                input_count += 1
    except:
        print(f'Directory {input_directory} not found')
        exit()

    print(f'Number of files in directory: {input_count}')
   
    output_directory = 'data/raw'

    if not os.path.isdir(output_directory):
        print('Output directory does not exist. Will create directory')
        os.mkdir(output_directory)

    print('Starting file conversion...')

    convert_files_in_folder(input_directory, output_directory)
        
    if input_directory == output_directory:
        output_count = 0
        for path in os.scandir(output_directory):
            if path.is_file():
                output_count += 1
        output_count = output_count - input_count
    else:
        output_count = 0
        for path in os.scandir(output_directory):
            if path.is_file():
                output_count += 1

    skipped_files = input_count - output_count

    print(f'{output_count} files converted, {skipped_files} files skipped')

    print(f"Enter 'delete' to delete original files")
    instruction = input()

    if instruction == 'delete':
        print('Deleting...')
        for file in file_list:
            os.remove(file)
    else:
        pass
   


if __name__ == '__main__':
    user_interface()