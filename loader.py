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
import base64
import json
import google.auth
import googleapiclient.discovery

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


# +

# Load the credentials from the credentials.json file

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


credentials_string = base64.b64decode(os.environ['CREDENTIALS_JSON']).decode('ascii')
credentials_json = json.loads(credentials_string)
pretty_json = json.dumps(credentials_json, indent=4)
print(pretty_json)


# Load the private key file
#with open("service_account.json") as f:
#    private_key = json.load(f)

private_key = credentials_json['private_key']

print("private key"+private_key)
# Create a ServiceAccountCredentials object
credentials = Credentials.from_service_account_info(credentials_json, scopes=["https://www.googleapis.com/auth/drive"])

# Get an access token from the credentials
#access_token = credentials.get_access_token().access_token

# Build the Google Drive API client using the access token
service = build("drive", "v3", credentials=credentials)

# Example API call
results = service.files().list(q="mimeType='application/vnd.google-apps.folder'", fields="nextPageToken, files(id, name)").execute()
folders = results.get("files", [])

# Print the name of the first folder
if folders:
    print(f"The first folder is named: {folders[0]['name']}")
else:
    print("No folders were found.")
# -




