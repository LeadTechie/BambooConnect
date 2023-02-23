# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:light
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
import time
import io
import base64
import json
import google.auth
import googleapiclient.discovery
from googleapiclient.http import MediaFileUpload
import unittest
import logging
import httplib2
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import support.authentication_support as auth_support

# -
# # !pip uninstall bamboo_connect -y



# +
# #!pip install bamboo_connect
# -

class Base_Extractor():
    cache_dir=""
    extract = ""
    extract_status_code = 0

    def __init__(self, cache_dir=""):
        self.cache_dir=cache_dir
        None


    #def extract(self, *argv):
    #    None

    def save_results_as_file(self, key_name):
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        file_path = os.path.join(self.cache_dir, key_name)
        with open(file_path, "w") as file:
            file.write(self.extract)

    def load_results_from_file(self, key_name):
        file_path = os.path.join(self.cache_dir, key_name)
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                self.extract = file.read()
                self.extract_status_code = 1
                return True
        else:
            return False

    def set_query_details(self, *argv):
        None


# +
def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Execution time: {end - start} seconds")
        return result
    return wrapper

@measure_time
def my_function():
    # Function implementation here
    time.sleep(2)

#my_function()


# -

class Google_Drive_File_Extractor(Base_Extractor):
    file_id = ""
    file_name = ""
    parents = []
    mimeType = ""
    credentials_json = ""


    def __init__(self, request_parameters, cache_dir=""):
        super().__init__(cache_dir=cache_dir)
        self.load_request_parameters(request_parameters)
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Request_Connector")

        
    def load_request_parameters(self, parameters):
        self.file_id = parameters['file_id'] if "file_id" in parameters else ""
        self.folder_id = parameters['folder_id'] if "folder_id" in parameters else ""
        self.file_name = parameters['file_name'] if "file_name" in parameters else ""
        self.parents = parameters['parents'] if "parents" in parameters else []
        self.mimeType = parameters['mimeType'] if "mimeType" in parameters else ""
        self.credentials_json = parameters['credentials_json'] if "credentials_json" in parameters else ""
        
    def get_google_drive_service(self):
        #print(json.dumps(credentials_json, indent=4))
        #service = get_google_drive_service(self.credentials_json)
        # Load the private key file        private_key = credentials_json['private_key']

        #print("private key"+private_key)
        # Create a ServiceAccountCredentials object
        credentials = Credentials.from_service_account_info(self.credentials_json, scopes=["https://www.googleapis.com/auth/drive"])

        # Get an access token from the credentials
        #access_token = credentials.get_access_token().access_token

        # Build the Google Drive API client using the access token
        service = build("drive", "v3", credentials=credentials)
        return service

    @measure_time
    def extract_data(self, cache_key=""):
        logging.debug("0")
        if self.extract_status_code == 0:
            logging.debug("1")
            if self.load_results_from_file(cache_key):
                logging.debug("2")
                logging.debug(self.extract)
                return self.extract
            else:
                temp_status = self.extract_from_web()
                if cache_key != "":
                    self.save_results_as_file(cache_key)
                logging.debug("3 "+ str(temp_status))
        logging.debug(self.extract)
        logging.debug(type(self.extract))
        return self.extract

    def get_response_status_code(self):
        return self.extract_status_code


    def get_file_content(self):
        service = self.get_google_drive_service()

        query = f"'{self.folder_id}' in parents and name='{self.file_name}'"
        results = service.files().list(q=query, fields="files(id)").execute()
        items = results.get("files", [])
        if not items:
            print(f"No file found with name '{file_name}' in folder with ID '{folder_id}'")
            return ""

        # Get the content of the first file matching the query
        file_id = items[0]["id"]
        file = service.files().get_media(fileId=file_id).execute()
        file_content = file.decode("utf-8")
        self.extract = file_content
        return file_content        
        

    def extract_from_web(self):
        self.get_file_content()
        return "200"

    






# +




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
        print("file_id")
        print(file_id)
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

def test_google_drive_data():
    credentials_json = decode_credentials_json()
    #print(json.dumps(credentials_json, indent=4))
    service = get_google_drive_service(credentials_json)
    list_all_directories_files(service)
    file_content = get_file_content("1GoXl2a3tsvJfvTqUYh3p4Dw2a1e7Pc0R")
    print(file_content)

    folder_id="1Ba27PI1No-5wkzEaop4zfKrcLZiB_-9z"
    save_file_in_folder(service, folder_id, "first_saved_file.txt", "Content is here and has been updated")

# -






# +

#if __name__ == "__main__":

