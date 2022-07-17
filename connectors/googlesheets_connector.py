# library modules
import os
import base64
import gspread
import json
import warnings
from connectors.base_connector import Base_Connector


class GoogleSheets_Connector(Base_Connector):
    # base class provides
    #.get_raw_data
    #.get_clean_data

    def __init__(self, gc_in = None):
        #Hack Fix! https://stackoverflow.com/questions/48160728/resourcewarning-unclosed-socket-in-python-3-unit-test
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        self.gc = gc_in
        self.clean_data = self.default_clean_data

    def initialse_auth(self, credentials_key='CREDENTIALS_JSON'):
        credentialsb64 = os.getenv(credentials_key)
        credentials = base64.b64decode(credentialsb64)
        json_credentials = json.loads(credentials)
        self.gc = gspread.service_account_from_dict(json_credentials)

    def initialse_query(self, get_raw_data_in_function, *argv):
        self.get_raw_data = self.curry(get_raw_data_in_function, *argv)


# generic support methods

    def get_worksheet_values(self, workbook_name, sheet_name):
        sh = self.gc.open(workbook_name)
        return sh.worksheet(sheet_name).get_all_values()


    def reset_sheet_data(self, workbook_name, sheet_name):
        #print("clearing data")
        sh = self.gc.open(workbook_name)
        sh.worksheet(sheet_name).clear()
        # worksheet1 = spreadsheet.worksheet('January')
        # worksheet2 = worksheet1.copy('February')

    def copy_sheet_data(self, workbook_name, sheet_name_from, sheet_name_to):
        sh = self.gc.open(workbook_name)
        values = sh.worksheet(sheet_name_from).get_all_values()
        sh.worksheet(sheet_name_to).update("A1", values)

    def update_data(self, workbook_name, sheet_name, start_ref, data_in):
        sh = self.gc.open(workbook_name)
        sh.worksheet(sheet_name).update(start_ref, data_in)

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
