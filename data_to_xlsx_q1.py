"""
This file imports the MASSIVE Dataset, contains all the constants necessary for the system, and functions for processing
Goes to the processed dataset, xlsx
"""

import concurrent.futures
import pandas as pd
import os
from absl import app
from flags_config import FLAGS

# Constants
dataset_dir = './amazon-dataset'
processed_files_dir = './processed-dataset'
english_dataset = 'en-US.jsonl'
german_dataset = 'de-DE.jsonl'
swahili_dataset = 'sw-KE.jsonl'
partitioned_dir = './partitioned_dataset'


# Functions

def build_file_path(file_name: str) -> str:
    return os.path.join(dataset_dir, file_name)


def read_jsonl_file(path: str) -> pd.DataFrame:
    df = pd.read_json(path, lines=True)
    return df


def merge_with_english(english_df: pd.DataFrame, other_df: pd.DataFrame) -> pd.DataFrame:
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


# Logic

def generate_xlsx_file(file: str) -> None:
    dataset_path = os.path.join(dataset_dir, file)
    df = read_jsonl_file(dataset_path)
    lang_code = file.split('-')[1].split('.')[0]
    english_jsonl = pd.read_json(f"{dataset_dir}/{english_dataset}", lines=True)
    df = merge_with_english(english_jsonl, df)

    # Ensure processed_files_dir exists before saving
    if not os.path.exists(processed_files_dir):
        os.makedirs(processed_files_dir)

    df.to_excel(f'{processed_files_dir}/en-{lang_code}.xlsx')


def process_all_files(data_dir: str):
    files = os.listdir(data_dir)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(generate_xlsx_file, files)


def main(_):
    process_all_files("amazon-dataset")


if __name__ == '__main__':
    app.run(main)