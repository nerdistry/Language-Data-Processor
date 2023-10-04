"""
This file imports the MASSIVE Dataset, contains all the constants necessary for the system, and functions for processing
Goes to the processed dataset, xlsx
"""

import concurrent.futures
import pandas as pd
import os
import itertools
import sys
import time
import logging
from absl import app
from flags_config import FLAGS

dataset_dir = './amazon-dataset'
processed_files_dir = './processed-dataset'
english_dataset = 'en-US.jsonl'
german_dataset = 'de-DE.jsonl'
swahili_dataset = 'sw-KE.jsonl'
partitioned_dir = './partitioned_dataset'

logging.basicConfig(level=logging.INFO)
spinner = itertools.cycle(['-', '/', '|', '\\'])

def build_file_path(file_name: str) -> str:
    '''The function takes a file name as input and returns the path by joining it with a directory (dataset_dir) using os.path.join().'''
    return os.path.join(dataset_dir, file_name)


def read_jsonl_file(path: str) -> pd.DataFrame:
    '''The function reads a JSON Lines file (path) into a pandas DataFrame (df) and returns that DataFrame.'''
    sys.stdout.write(next(spinner))
    sys.stdout.flush()
    time.sleep(0.15)
    sys.stdout.write('\b')

    df = pd.read_json(path, lines=True)
    return df


def merge_with_english(english_df: pd.DataFrame, other_df: pd.DataFrame) -> pd.DataFrame:
    '''
    The function merges two DataFrames (english_df and other_df) based on a common "id",
    renames columns, selects specific columns, and returns the merged DataFrame.
    '''
    df = other_df.set_index('id').join(english_df.set_index('id'), rsuffix='_english')
    df = df.rename(columns={
        "utt_english": "utt_translation",
        "annot_utt_english": "annot_utt_translation",
        "utt": "utterance",
        "annot_utt": "annot_utt",
    })
    df.reset_index(inplace=True)
    df = df[["id", "utterance", "utt_translation", "annot_utt_translation", "annot_utt", "partition"]]
    return df

def generate_xlsx_file(file: str) -> None:
    '''The function processes a JSON Lines file, merges it with an English dataset, and saves the merged data into an Excel file.'''
    sys.stdout.write(next(spinner))
    sys.stdout.flush()
    time.sleep(0.15)
    sys.stdout.write('\b')
    dataset_path = os.path.join(dataset_dir, file)
    df = read_jsonl_file(dataset_path)
    lang_code = file.split('-')[1].split('.')[0]
    english_jsonl = pd.read_json(f"{dataset_dir}/{english_dataset}", lines=True)
    df = merge_with_english(english_jsonl, df)


    if not os.path.exists(processed_files_dir):
        os.makedirs(processed_files_dir)
    df.to_excel(f'{processed_files_dir}/en-{lang_code}.xlsx')


def process_all_files(data_dir: str):
    '''The function processes all files in a directory concurrently, using multiprocessing, by generating Excel files for each JSON Lines file in the directory.'''
    files = os.listdir(data_dir)
    logging.info("Running data_to_xlsx_q1.py script...")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(generate_xlsx_file, files)
    logging.info("Conversion to .xlsx complete!")


def main(_):
    process_all_files("amazon-dataset")


if __name__ == '__main__':
    app.run(main)