import os

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

gauth = GoogleAuth()

secrets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "secrets")
gauth.DEFAULT_SETTINGS['client_config_file'] = os.path.join(secrets_dir, "client_secrets.json")
gauth.DEFAULT_SETTINGS['save_credentials'] = True
gauth.DEFAULT_SETTINGS['save_credentials_backend'] = 'file'
gauth.DEFAULT_SETTINGS['save_credentials_file'] = os.path.join(secrets_dir, "credentials.json")
gauth.DEFAULT_SETTINGS['get_refresh_token'] = True

gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)


def send_to_drive(filename: str):
    with open(filename, "rb") as f:
        file_drive = drive.CreateFile({'title': os.path.splitext(os.path.basename(f.name))[0]})
        file_drive.SetContentFile(filename)
        file_drive.Upload()
        permission = file_drive.InsertPermission({
            'type': 'anyone',
            'value': 'anyone',
            'role': 'reader'})
        link = file_drive['alternateLink']
        return link