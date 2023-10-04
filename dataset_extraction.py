import itertools
import sys
import time
from absl import app, flags

import pandas as pd
import tarfile
import os


FLAGS = flags.FLAGS
flags.DEFINE_string('tarfile_path', 'data/amazon_massive_dataset.tar.gz', 'Path to the tar.gz file that needs to be extracted.')
def extract_dataset(filename: str) -> list:
    """
    Extracts the dataset and returns the list of extracted jsonl files.
    """

    extracted_files = []
    destination_dir = "amazon-dataset"

    spinner = itertools.cycle(['-', '/', '|', '\\'])



    with tarfile.open(filename, "r:gz") as tar:
        for member in tar.getmembers():
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            time.sleep(0.15)
            sys.stdout.write('\b')
            if member.isfile() and member.name.endswith('.jsonl'):
                # Modify member's name to just the filename to prevent directory structure replication
                member.name = os.path.basename(member.name)
                tar.extract(member, path=destination_dir)
                extracted_files.append(member.name)

    return extracted_files


extracted_files = extract_dataset("data/amazon_massive_dataset.tar.gz")