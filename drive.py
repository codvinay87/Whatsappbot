import os
import gspread

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from googleapiclient.http import MediaFileUpload
from servicecredentials import Create_Service
def upload(filename,price,col_a,col_b):

    CLIENT_SECRET_FILE = 'client_secret.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    folder_id = "1OhFbu4KWxr48RUyOIo__kASRbZIhBfkd"
    file_name = 'uploads/.jpg'
    file_mime = "image/jpeg"
    file_metadata = {
        'name': filename,
        'parents': [folder_id]
    }
    media = MediaFileUpload('./{0}'.format(file_name), mimetype=file_mime)
    service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    gc = gspread.service_account(filename='private_key.json')
    wks = gc.open("SwastikJewellery").sheet1
    col_a=len(wks.get("A:A"))+1
    col_b=len(wks.get('B:B'))+1
    wks.update('A{0}'.format(col_a),filename)
    wks.update('B{0}'.format(col_b), price)

    os.remove('uploads/.jpg')
