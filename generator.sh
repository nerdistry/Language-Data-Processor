
logging.info("Extracting tar.gz file")
python dataset_extraction.py --tarfile_path=data/amazon_massive_dataset.tar.gz
logging.info("Extraction completed.")


logging.info("Running data_to_xlsx_q1.py script...")
python data_to_xlsx_q1.py \
    --dataset_dir=amazon-dataset \
    --output_dir=processed-dataset
logging.info("Convertion to .xlsx complete!")


logging.info("Generating separate jsonl files...")
python jsonl_gen_q2.py \
    --input_directory=amazon-dataset \
    --output_directory=languages \
    --languages=en-US,sw-KE,de-DE \
    --partitions=test,train,dev
logging.info("Generated separate jsonl files!!")


logging.info("Generating separate jsonl files...")
python en_to_xx_train_q3.py \
    --processed_files_dir=processed-dataset \
    --english_dataset=en_to_xx_translations.json 
logging.info("Generating separate jsonl files...")


python drive_backup.py --zip_filename=group5cat.zip

logging.info "All scripts executed successfully!"
