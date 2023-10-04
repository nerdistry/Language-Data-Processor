
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

FLAGS = flags.FLAGS

flags.DEFINE_string("backup_directory", ".", "The directory to backup.")
flags.DEFINE_string("zip_filename", "backup.zip", "The filename for the zipped backup.")

def zipdir(path, ziph):
    # Zip the directory
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), path))

#User authentication using google API
def authenticate():
    creds = None
    token_path = "token.json"
    credentials_path = "client_secret.json"

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path,
                                                             ["https://www.googleapis.com/auth/drive.file"])
            creds = flow.run_local_server(port=0)

        with open(token_path, "w") as token:
            token.write(creds.to_json())

    return creds

# zipping the project folder and and uploading the files to google drive

def upload_to_drive(file_path):
    creds = authenticate()
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
        print(f'Upload of {zip_filename} to google drive failed ')
        

if __name__ == "__main__":
    directory_to_backup = '.'  # Current directory
    zip_filename = 'group5cat.zip'

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir(directory_to_backup, zipf)

    upload_to_drive(zip_filename)
    print('Upload of group5cat.zip to google drive completed with success')
