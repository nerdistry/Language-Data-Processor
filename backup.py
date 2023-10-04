
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