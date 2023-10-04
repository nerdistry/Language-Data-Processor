#!/bin/bash

# Extract the tar.gz file
python dataset_extraction.py --tarfile_path=data/amazon_massive_dataset.tar.gz

# Run the first Python script
python data_to_xlsx_q1.py \
    --dataset_dir=amazon-dataset \
    --output_dir=processed-dataset

# Run the second Python script
python jsonl_gen_q2.py \
    --input_directory=amazon-dataset \
    --output_directory=languages \
    --languages=en-US,sw-KE,de-DE \
    --partitions=test,train,dev

