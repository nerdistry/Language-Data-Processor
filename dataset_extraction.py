"""
This module provides functionality to extract specific `.jsonl` files from a given tarball.
"""
import itertools
from absl import flags
import tarfile
import os
import logging

logging.basicConfig(level=logging.INFO)

FLAGS = flags.FLAGS
flags.DEFINE_string('tarfile_path',
                    'data/amazon_massive_dataset.tar.gz',
                    'Path to the tar.gz file that needs to be extracted.')
def extract_dataset(filename: str) -> list:
    """Extracts the dataset and returns the list of extracted jsonl files. """
    extracted_files = []
    destination_dir = "amazon-dataset"

    logging.info("Extracting Dataset")
    spinner = itertools.cycle(['-', '/', '|', '\\'])

    with tarfile.open(filename, "r:gz") as tar:
        for member in tar.getmembers():
            if member.isfile() and member.name.endswith('.jsonl'):
                member.name = os.path.basename(member.name)
                tar.extract(member, path=destination_dir)
                extracted_files.append(member.name)

    logging.info(f"Extraction to \"{destination_dir}\" Completed Successfully")
    return extracted_files

extracted_files = extract_dataset("data/amazon_massive_dataset.tar.gz")