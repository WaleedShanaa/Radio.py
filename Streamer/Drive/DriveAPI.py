from googleapiclient.http import MediaFileUpload
from Google import Create_Service


CLIENT_SECRET_FILE = 'Drive//client_secret.json'# your json file (download it to the Drive directory )
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
folder_id = '' # the folder you want to upload the songs to

def SendToDrive(Name):
    page_token = None
    while True:
        response = service.files().list(
                                            q=" 'folder name' in parents and trashed = false",
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name)',
                                            pageToken=page_token).execute()

        for file in response.get('files', []):
            if(file.get('name')==Name):
                return

        file_name = f'Drive//Songs//{Name}'

        file_metadata = {
            'name': file_name.split("//")[-1],
            'parents': [folder_id]
        }
        media = MediaFileUpload('{}'.format(file_name))

        service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()




