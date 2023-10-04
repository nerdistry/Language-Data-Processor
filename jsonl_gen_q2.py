import os
import json
from absl import app
from flags_config import FLAGS

input_directory = 'amazon-dataset'
output_directory = 'languages'

os.makedirs(output_directory, exist_ok=True)

languages = set(['en-US', 'sw-KE', 'de-DE'])
partitions = ['test', 'train', 'dev']

def filter_and_save_records(input_file, language):
    # Open all the output files for the current language at once
    output_files = {
        partition: open(os.path.join(output_directory, f'{language}-{partition}.jsonl'), 'w', encoding='utf-8')
        for partition in partitions}

    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            record = json.loads(line)
            if record['locale'].startswith(language) and record['partition'] in output_files:
                json.dump(record, output_files[record['partition']])
                output_files[record['partition']].write('\n')

    # Close all the output files for the current language
    for file in output_files.values():
        file.close()


for language in languages:
    input_file = os.path.join(input_directory, f'{language}.jsonl')
    filter_and_save_records(input_file, language)

def main(argv):
    os.makedirs(FLAGS.output_directory, exist_ok=True)

    for language in FLAGS.languages:
        input_file = os.path.join(FLAGS.input_directory, f'{language}.jsonl')
        filter_and_save_records(input_file, language)

    print('JSONL files have been generated and saved to', FLAGS.output_directory)

