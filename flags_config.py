from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_string('dataset_dir', './amazon-dataset', 'Directory of the dataset.')
flags.DEFINE_string('english_dataset', 'en-US.jsonl', 'Filename of the English dataset.')
flags.DEFINE_string('output_dir', './processed-dataset', 'Directory to save the processed files.')

flags.DEFINE_string("input_directory", './amazon-dataset', "Path to the input directory containing JSONL files")
flags.DEFINE_string("output_directory", './languages', "Path to the directory where split JSONL files will be saved")
flags.DEFINE_list("languages", ['en-US', 'sw-KE', 'de-DE'], "List of languages to be processed")
flags.DEFINE_list("partitions", ["train", "test", "dev"], "List of partitions to be generated")

flags.DEFINE_string(
    'processed_files_dir',
    default='processed-dataset',
    help='Path to the directory containing processed .xlsx files'
)