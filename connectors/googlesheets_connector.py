# library modules
import os
import base64
import gspread
import json
import warnings
from connectors.base_connector import Base_Connector


class GoogleSheets_Connector(Base_Connector):

    def __init__(self):
        #Hack Fix! https://stackoverflow.com/questions/48160728/resourcewarning-unclosed-socket-in-python-3-unit-test
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        self.gc = None
    #
    def initialse_auth(self):
        credentialsb64 = os.getenv('CREDENTIALS_JSON')
        credentials = base64.b64decode(credentialsb64)
        json_credentials = json.loads(credentials)
        self.gc = gspread.service_account_from_dict(json_credentials)

    def set_auth_details(*argv):
        None

    def clean_data():
        None

    def get_raw_data(self, *args):
        return self.get_worksheet_values(*args)

    def get_worksheet_values(self, workbook_name, sheet_name):
        sh = self.gc.open(workbook_name)
        return sh.worksheet(sheet_name).get_all_values()

    def get_clean_data():
        return []

# -> Below still to refactor clean up

    #Update values https://docs.gspread.org/en/latest/user-guide.html#getting-all-values-from-a-worksheet-as-a-list-of-lists
    # worksheet.update('A1:B2', [[1, 2], [3, 4]])
    def get_sheet(self, workbook_name, sheet_name):
        sh = self.gc.open(workbook_name)
        return sh.worksheet(sheet_name).get_all_values()


    def update_cells(self, workbook_name, sheet_name, cell_ref, cells):
        sh = self.gc.open(workbook_name)
        worksheet = sh.worksheet(sheet_name)
        #'A1:B2', [[1, 2], [3, 4]]
        worksheet.update(cell_ref, cells)

    def get_cell(self, workbook_name, cell_ref):
        sh = self.gc.open(workbook_name)
        return sh.sheet1.get(cell_ref)
