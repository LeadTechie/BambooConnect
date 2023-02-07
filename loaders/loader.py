# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
# !pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client





import os
import io
import base64
import json
import google.auth
import googleapiclient.discovery
from googleapiclient.http import MediaFileUpload

# +
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build



credentials_string = base64.b64decode(os.environ['CREDENTIALS_JSON']).decode('ascii')
credentials_json = json.loads(credentials_string)
pretty_json = json.dumps(credentials_json, indent=4)
print(pretty_json)



creds = Credentials.from_authorized_user_info(credentials_json)

# Build the Google Drive API client
service = build("drive", "v3", credentials=creds)

# Create the subfolder
folder_metadata = {
    "name": "example_subfolder",
    "mimeType": "application/vnd.google-apps.folder",
    "parents": ["root"]
}

folder = service.files().create(body=folder_metadata, fields="id").execute()

# Get the subfolder ID
subfolder_id = folder["id"]

# Define the file metadata
file_metadata = {
    "name": "example.txt",
    "parents": [subfolder_id],
    "mimeType": "text/plain"
}

# Define the file content
file_content = "Example content for the file.".encode("utf-8")

# Create the file in Google Drive
file = service.files().create(body=file_metadata, media_body=file_content, fields="id").execute()

# Print the file ID
print("File ID:", file["id"])

# -







# +

from googleapiclient.discovery import build
#from google.oauth2.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
import json


def decode_credentials_json():
    credentials_string = base64.b64decode(os.environ['CREDENTIALS_JSON']).decode('ascii')
    credentials_json = json.loads(credentials_string)
    #pretty_json = json.dumps(credentials_json, indent=4)
    #print(pretty_json)
    return credentials_json

def get_google_drive_service(credentials_json):
    # Load the private key file
    #with open("service_account.json") as f:
    #    private_key = json.load(f)

    private_key = credentials_json['private_key']

    #print("private key"+private_key)
    # Create a ServiceAccountCredentials object
    credentials = Credentials.from_service_account_info(credentials_json, scopes=["https://www.googleapis.com/auth/drive"])

    # Get an access token from the credentials
    #access_token = credentials.get_access_token().access_token

    # Build the Google Drive API client using the access token
    service = build("drive", "v3", credentials=credentials)
    return service

def list_all_directories_files(service):
    # Example API call
    results = service.files().list(q="mimeType='application/vnd.google-apps.folder'", fields="nextPageToken, files(id, name)").execute()
    folders = results.get("files", [])

    # Print the name of the first folder
    if folders:
        for folder in folders:
            folder_id = folder['id'] 
            print(f"The first folder is named: {folder}")
            results = service.files().list(q=f"'{folder_id}' in parents", fields="nextPageToken, files(id, name)").execute()
            files = results.get("files", [])
            print(files)
            # Print the names of the files in the folder
            if files:
                print("The files in the folder are:")
                for file in files:
                    print(file)
            else:
                print("No files were found in the folder.")

    else:
        print("No folders were found.")


    folder_id = folders[0]['id'] #"FOLDER_ID"

    # Example API call to list files in the folder    

def get_file_content(id):

    json_test_file_id = "1GoXl2a3tsvJfvTqUYh3p4Dw2a1e7Pc0R"

    file = service.files().get(fileId=json_test_file_id, fields='*').execute()

    # Get the content of the file as a string
    file_content = file.get('content')
    #print(json.dumps(file, indent=4))

    file = service.files().get_media(fileId=json_test_file_id).execute()
    file_content = file.decode('utf-8')
    return file_content


from io import BytesIO

def save_file_in_folder(service, folder_id, file_name, file_content):
    mimeType = ""
    if file_name[-4:]=="json":
        mimeType = "application/json"
    else:
        mimeType ="text/plain"
    
    file_metadata = {
        "name": file_name,
        "parents": [folder_id],
        "mimeType": mimeType
    }
    
    with open(file_name, "w") as file:
        file.write(file_content)

    file_id = get_file_by_name(service, file_name, folder_id)

    if file_id:
        #file_metadata['id'] = file_id['id']
        media = MediaFileUpload(file_name, mimetype=mimeType)
        file = service.files().update(fileId=file_id['id'], media_body=media).execute()
    else:
        media = MediaFileUpload(file_name, mimetype=mimeType)
        file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()    
    
    print(f"File ID: {file['id']}")
    return file
 
def get_file_by_name(service, file_name, folder_id):
    query = "name='" + file_name + "' and trashed = false and parents in '" + folder_id + "'"
    results = service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
    items = results.get("files", [])
    if not items:
        return None
    return items[0]    

credentials_json = decode_credentials_json()
#print(json.dumps(credentials_json, indent=4))
service = get_google_drive_service(credentials_json)
list_all_directories_files(service)
file_content = get_file_content("1GoXl2a3tsvJfvTqUYh3p4Dw2a1e7Pc0R")
print(file_content)

folder_id="1Ba27PI1No-5wkzEaop4zfKrcLZiB_-9z"
save_file_in_folder(service, folder_id, "first_saved_file.txt", "Content is here and has been updated")
    

# -




