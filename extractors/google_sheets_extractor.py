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

# First, install the required libraries
# !pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Import the libraries
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


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
            if len(file_path)>3 and file_path[-4:] == "json":
                json.dump(self.extract, file)
            else:
                file.write(self.extract)

    def load_results_from_file(self, key_name):
        file_path = os.path.join(self.cache_dir, key_name)
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                if len(file_path)>3 and file_path[-4:] == "json":
                    self.extract = json.load(file)
                    self.extract_status_code = 1
                else:
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

my_function()


# -

class Google_Sheets_Extractor(Base_Extractor):
    file_id = ""
    tab_name = ""
    data_range = ""
    credentials_json = ""

    def __init__(self, request_parameters, cache_dir=""):
        super().__init__(cache_dir=cache_dir)
        self.load_request_parameters(request_parameters)
        logging.debug("Request_Connector")

    def load_request_parameters(self, parameters):
        self.file_id = parameters['file_id'] if "file_id" in parameters else ""
        self.tab_name = parameters['tab_name'] if "tab_name" in parameters else ""
        self.data_range = parameters['data_range'] if "data_range" in parameters else []
        self.credentials_json = parameters['credentials_json'] if "credentials_json" in parameters else []

    def get_google_drive_service(self):
        creds = Credentials.from_service_account_info(self.credentials_json, scopes=["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"])
        sheets_service = build("sheets", "v4", credentials=creds)
        return sheets_service

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

    def decode_credentials_json():
        credentials_string = base64.b64decode(os.environ['CREDENTIALS_JSON']).decode('ascii')
        credentials_json = json.loads(credentials_string)
        #pretty_json = json.dumps(credentials_json, indent=4)
        #print(pretty_json)
        return credentials_json

    def get_sheets_content(self):
        #Build the Google Sheets API client
        sheets_service = self.get_google_drive_service()
        #sheets_service = build("sheets", "v4", credentials=creds)

        # Define the range to read
        range_ = self.tab_name+"!"+self.data_range

        # Call the Sheets API to get the values
        result = sheets_service.spreadsheets().values().get(spreadsheetId=self.file_id, range=range_).execute()

        # Get the values from the API result
        values = result.get("values", [])

        # Print the values
        for row in values:
            print(row)
        self.extract = values
        return self.extract

    def extract_from_web(self):
        self.get_sheets_content()
        print(type(self.get_sheets_content()))
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

#credentials_json = decode_credentials_json()
#print(json.dumps(credentials_json, indent=4))
#service = get_google_drive_service(credentials_json)
#list_all_directories_files(service)
#file_content = get_file_content("1GoXl2a3tsvJfvTqUYh3p4Dw2a1e7Pc0R")
#print(file_content)

#folder_id="1Ba27PI1No-5wkzEaop4zfKrcLZiB_-9z"
#save_file_in_folder(service, folder_id, "first_saved_file.txt", "Content is here and has been updated")

# -




# +
class Test_Google_Sheets_Extractor(unittest.TestCase):

    def test_Google_Sheets_Extractor(self):
        expected = [['Bamboo Test A1', 'Bamboo Test B1'],
                    ['Bamboo Test A2', 'Bamboo Test B2']]

        parameters = {
            "file_id": "12keD9VYi6yrQ4nP7JJh95M8lmyTqIJw-V4IocOcyjYM",
            "tab_name": "sheet1",
            "data_range": "A1:B2",
            "credentials_json": decode_credentials_json()
        }
        gdse = Google_Sheets_Extractor(parameters,"test_data")
        #sheets_content = gdse.extract_data("google_sheets_file.json")
        sheets_content = gdse.extract_data()
        self.assertEqual(sheets_content, expected, "Content should be read from file from Google Drive")


#logging.basicConfig(level=logging.ERROR)
# -
























#logging.basicConfig(level=logging.ERROR)























# +

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)
# -

# from transform.recon_dataset import Recon_DataSet
# from transform import data_translations
