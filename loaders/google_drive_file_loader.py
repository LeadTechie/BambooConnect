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
import time
import io
import base64
import json
import google.auth
import googleapiclient.discovery
from googleapiclient.http import MediaFileUpload
import unittest
import logging

from googleapiclient.discovery import build
#from google.oauth2.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
import json
# -



class Base_Loader():
    cache_dir=""
    file_content = ""
    file_name = ""
    save_status_code = 0

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
    time.sleep(0.2)

#my_function()


# -

class Google_Drive_File_Loader(Base_Loader):
    folder_id = ""
    mimeType = ""
    parent_id = ""
    credentials_json = ""


    def __init__(self, request_parameters, cache_dir=""):
        super().__init__(cache_dir=cache_dir)
        self.load_request_parameters(request_parameters)
        logging.debug("Request_Connector")

    def load_request_parameters(self, parameters):
        self.file_name = parameters['file_name'] if "file_name" in parameters else ""
        self.parent_id = parameters['parent_id'] if "parent_id" in parameters else ""
        self.mimeType = parameters['mimeType'] if "mimeType" in parameters else ""
        self.credentials_json = parameters['credentials_json'] if "credentials_json" in parameters else ""
        self.file_content = parameters['file_content'] if "file_content" in parameters else ""
        self.folder_id = parameters['folder_id'] if "folder_id" in parameters else ""

    def get_google_drive_service(self):
        credentials = Credentials.from_service_account_info(self.credentials_json, scopes=["https://www.googleapis.com/auth/drive"])
        # Build the Google Drive API client using the access token
        service = build("drive", "v3", credentials=credentials)
        return service

    @measure_time
    def save_data(self, file_content):
        self.file_content = file_content
        self.save_file_in_folder()
        return self.file_content

    def get_response_status_code(self):
        return self.save_status_code


    def get_file_by_name(self, service, file_name, folder_id):
        query = "name='" + file_name + "' and trashed = false and parents in '" + folder_id + "'"
        results = service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
        items = results.get("files", [])
        if not items:
            return None
        return items[0]

    def save_file_in_folder(self):
        mimeType = ""
        if self.file_name[-4:]=="json":
            mimeType = "application/json"
        else:
            mimeType ="text/plain"

        file_metadata = {
            "name": self.file_name,
            "parents": [self.folder_id],
            "mimeType": self.mimeType
        }

        with open(self.file_name, "w") as file:
            file.write(self.file_content)

        #if file already exists, then overwrite rathert than create a 2nd copy
        file_id = self.get_file_by_name(self.get_google_drive_service(), self.file_name, self.folder_id)

        if file_id:
            #file_metadata['id'] = file_id['id']
            media = MediaFileUpload(self.file_name, mimetype=mimeType)
            file = self.get_google_drive_service().files().update(fileId=file_id['id'], media_body=media).execute()
        else:
            print ("creating file")
            media = MediaFileUpload(self.file_name, mimetype=mimeType)
            file = self.get_google_drive_service().files().create(body=file_metadata, media_body=media, fields="id").execute()

        print ("returning file")
        return file

    def extract_from_web(self):
        self.get_file_content()
        return "200"



    def decode_credentials_json():
        credentials_string = base64.b64decode(os.environ['CREDENTIALS_JSON']).decode('ascii')
        credentials_json = json.loads(credentials_string)
        #pretty_json = json.dumps(credentials_json, indent=4)
        #print(pretty_json)
        return credentials_json






























# +



# Support function. Needs updating and testing

#logging.basicConfig(level=logging.ERROR)

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


# -





















# +

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)
# -

# from transform.recon_dataset import Recon_DataSet
# from transform import data_translations
