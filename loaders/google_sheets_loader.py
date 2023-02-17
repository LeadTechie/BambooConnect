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


def decode_credentials_json():
    credentials_string = base64.b64decode(os.environ['CREDENTIALS_JSON']).decode('ascii')
    credentials_json = json.loads(credentials_string)
    #pretty_json = json.dumps(credentials_json, indent=4)
    #print(pretty_json)
    return credentials_json

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

class Google_Sheets_Loader(Base_Loader):
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


    def save_data(self, data_in):
        self.file_content = data_in
        #Build the Google Sheets API client
        sheets_service = self.get_google_drive_service()
        #sheets_service = build("sheets", "v4", credentials=creds)

        # Define the range to read
        range_ = self.tab_name+"!"+self.data_range

        body = {
            'range': range_,
            'values': self.file_content,
            'majorDimension': 'ROWS'
        }

        # Call the Sheets API to get the values
        result = sheets_service.spreadsheets().values().update(spreadsheetId=self.file_id, range=range_, body=body, valueInputOption='RAW').execute()
        print (result)
        return result

    def extract_from_web(self):
        self.save_data(self.file_content)
        print(type(self.get_sheets_content()))
        return "200"


# +
class Test_Google_Sheets_Loader(unittest.TestCase):

    def test_Google_Sheets_Loader(self):
        data_to_save = [['Bamboo Test E1', 'Bamboo Test F1'],
                        ['Bamboo Test E2', 'Bamboo Test F2']]

        parameters = {
            "file_id": "12keD9VYi6yrQ4nP7JJh95M8lmyTqIJw-V4IocOcyjYM",
            "tab_name": "Sheet1",
            "data_range": "E1:F2",
            "credentials_json": decode_credentials_json()
        }
        gdse = Google_Sheets_Loader(parameters,"../test_data")
        result = gdse.save_data(data_to_save)
        expected = ""
        self.assertEqual(result['updatedCells'], 4, "It should return that 4 cells were updated")


#logging.basicConfig(level=logging.ERROR)



























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
