"""
This script filters records from input JSONL files for English (en), Swahili (sw), and German (de) based on their
partitions, and outputs separate JSONL files for each language and the respective partition
"""
import os
import json
import logging
from absl import app
from flags_config import FLAGS

logging.basicConfig(level=logging.INFO)

def filter_and_save_records(input_file, language):
    """
    Filters records from an input JSONL file by matching the 'locale' field with a specified language prefix
    and save them into separate JSONL files based on their 'partition' field.
    """
    output_files = {
        partition: open(os.path.join(FLAGS.output_directory, f'{language}-{partition}.jsonl'), 'w', encoding='utf-8')
        for partition in FLAGS.partitions}

    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            record = json.loads(line)
            if record['locale'].startswith(language) and record['partition'] in output_files:
                json.dump(record, output_files[record['partition']])
                output_files[record['partition']].write('\n')

    for file in output_files.values():
        file.close()

def main(argv):
    """
    Iterates through the provided languages, reads input JSONL files for each language,
    filters records using filter_and_save_records() function
    """
    os.makedirs(FLAGS.output_directory, exist_ok=True)
    logging.info("Generating separate jsonl files...")
    for language in FLAGS.languages:
        input_file = os.path.join(FLAGS.input_directory, f'{language}.jsonl')
        filter_and_save_records(input_file, language)

    logging.info('JSONL files have been generated and saved to %s', FLAGS.output_directory)

if __name__ == "__main__":
    app.run(main)
