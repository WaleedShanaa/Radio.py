import io
import os.path
import os
from googleapiclient.http import MediaIoBaseDownload
from Google import Create_Service


ClientSecretFile='Drive//client_secret.json'
APIName='drive'
APIVersion='v3'
Scopes=['https://www.googleapis.com/auth/drive']
service=Create_Service(ClientSecretFile,APIName,APIVersion,Scopes)

def Download():

	page_token = None

	Directory=os.listdir("Drive//Songs")

	response = service.files().list(
										q=" '1-vbzAogF5LAjmbbdK1N8rslrFNs2tf-m' in parents and trashed = false",
										spaces='drive',
										fields='nextPageToken, files(id, name)',
										pageToken=page_token).execute()

	for song in response.get('files', []):
		FileID=song.get("id")
		FileName = song.get("name")
		if FileName not in Directory:
			request = service.files().get_media(fileId=FileID)
			fh = io.BytesIO()
			Downloader = MediaIoBaseDownload(fd=fh, request=request)

			Done = False

			while not Done:
				status, Done = Downloader.next_chunk()

			fh.seek(0)

			with open(os.path.join("Drive//Songs", FileName), "wb") as f:
				f.write(fh.read())
				f.close()


	print("Download Completed")









