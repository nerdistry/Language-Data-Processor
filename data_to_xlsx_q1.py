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

