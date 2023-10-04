#!/bin/bash

# Extract the tar.gz file
python dataset_extraction.py --tarfile_path=data/amazon_massive_dataset.tar.gz

# Run the first Python script
python data_to_xlsx_q1.py \
    --dataset_dir=amazon-dataset \
    --output_dir=processed-dataset

