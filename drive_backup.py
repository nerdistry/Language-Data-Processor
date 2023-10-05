
import os
import zipfile
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
import logging
from absl import flags

"""
The 3 lines below are for defining command-line flags.
They specify values for certain variables when they run the script.
"""
FLAGS = flags.FLAGS

flags.DEFINE_string("backup_directory", ".", "The directory to backup.")
flags.DEFINE_string("zip_filename", "backup.zip", "The filename for the zipped backup.")

logging.basicConfig(level=logging.INFO)

def zipdir(path, ziph):
    """
    This function zips the content of the project directory. 
    It traverses the directory structure (os.walk) and adds files to the zip archive.
    """
    logging.info("Zipping the files")
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == zip_filename:  # Skip zipping the backup zip file itself.
                continue
            ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), path))

    logging.info("File zipped to group5cat.zip")


def authenticate():
    """
    This function is responsible for authenticating the user with the Google API, 
    It checks for an existing token (from token.json). 
    """
    logging.info("Authenticating...")
    creds = None
    token_path = "token.json"
    credentials_path = "client_secret.json"

    logging.info("Validating Token")
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path,["https://www.googleapis.com/auth/drive.file"])
            creds = flow.run_local_server(port=0)

        with open(token_path, "w") as token:
            token.write(creds.to_json())

    logging.info("Authentication Complete")
    return creds


def upload_to_drive(file_path):
    """
    This function is used to upload a specified file to G   oogle Drive.
    It defines the metadata for the file and then uses Google Drive's API to upload it.
    If the upload is successful, it logs the uploaded file's ID; if there's an error during upload, it logs a warning.
    """
    logging.info("Uploading to Google Drive")
    creds = authenticate()
    logging.info("Continuing Upload to Google Drive")
    drive_service = build("drive", "v3", credentials=creds)

    file_metadata = {
        'name': os.path.basename(file_path),
        'mimeType': 'application/octet-stream'
    }

    media = MediaFileUpload(file_path, mimetype='application/octet-stream', resumable=True)

    try:
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        logging.info(f"File {os.path.basename(file_path)} uploaded successfully with ID {file.get('id')}")
    except HttpError as error:
        logging.warning(f'Upload of {zip_filename} to google drive failed ')


if __name__ == "__main__":
    """
    This is the main entry point of the script when it's run as a standalone program.

    """
    directory_to_backup = '.'  # Current direcory
    zip_filename = 'group5cat.zip'

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
        zipdir(directory_to_backup, zipf)

    upload_to_drive(zip_filename)
    logging.info('Upload of group5cat.zip to google drive completed with success')
 
