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

import pandas as pd
import numpy as np
import json
import os
import unittest
import logging
import gspread
import sys
import os
import pathlib
# +
# #!pip install gspread

# Relative import work around if running interactively in Jupyter
def running_in_jupyter():
    try:
        get_ipython()
        return True
    except NameError:
        return False

if running_in_jupyter():
    # Go up two levels, import class then return to original subdirectory
    print(os.getcwd())
    os.chdir("..")
    print(os.getcwd())
    try:
        import support.authentication_support as auth_sup
        import transformers.data_translations as dt
        from extractors.google_sheets_extractor import Google_Sheets_Extractor
        from loaders.google_sheets_loader import Google_Sheets_Loader
        from extractors.extractor import Request_Extractor
    except Exception as e:
        print(e)
    finally:
        print("Finally - returning to project dir")
        print(os.getcwd())
        os.chdir("./samples")
        print(os.getcwd())
    print("Imported Jupyter Version")
else:
    #Assumes script running from main project directory
    import support.authentication_support as auth_sup
    import transformers.data_translations as dt
    from extractors.google_sheets_extractor import Google_Sheets_Extractor
    from loaders.google_sheets_loader import Google_Sheets_Loader
    from extractors.extractor import Request_Extractor
    print("Imported Non Jupyter Version")

# -



# from transform.recon_dataset import Recon_DataSet
# from transform import data_translations

def load_google_data():
    expected = [['TestComponent1'],
                ['TestComponent2'],
                ['TestComponent3']]

    parameters = {
        "file_id": "1CeClWOxaysZztz5V_wxfSvFmd8KzntLc3J67rkhukq4",
        "tab_name": "sheet1",
        "data_range": "A2:E",
        "credentials_json": auth_sup.decode_credentials_json()
    }
    gdse = Google_Sheets_Extractor(parameters,"../test_data/")
    sheets_content = gdse.extract_data()
    google_sheets_df = pd.DataFrame(sheets_content)
    google_sheets_df_updated = dt.process_component_sheets_data(google_sheets_df)
    print(google_sheets_df_updated)
    return google_sheets_df_updated





# +
def generate_params_for_jira_component_list(email, token):
    request_params = {}
    request_params['headers'] = {}
    request_params['data'] = {}
    request_params['url'] = "https://leadtechie.atlassian.net/rest/api/3/project/TEST/components"
    request_params['post_type']="GET"
    request_params['auth'] = (email, token)
    request_params['headers'] =  {
            "Accept": "application/json",
            'Content-Type': 'application/json'
        }
    return request_params

def load_jira_data():
    jira_token = os.environ['JIRA_TOKEN']
    jira_email = os.environ['JIRA_EMAIL']
    request_params = generate_params_for_jira_component_list(jira_email, jira_token)

    re_components = Request_Extractor(request_params, cache_dir="./test_data/")
    components_string = re_components.extract_data("")
    components_json = json.loads(components_string)
    pretty_json = json.dumps(components_json, indent=4)
    flattened_result = dt.flatten_jira_components(components_json)
    pretty_json = json.dumps(flattened_result, indent=4)
    print (pretty_json)
    df = pd.DataFrame(flattened_result)
    df1 = dt.process_jira_components_data(df)
    return df1


# -



def print_both_datasets(rds1, rds2):
    print("JIRA")
    print(rds2)
    print()
    print("Google")
    print(rds1)
    print()

def do_the_reconciliation(rds1, rds2):
    print_both_datasets(rds1, rds2)
    result = dt.update_add_delete_data(rds2, rds1)
    #print("result...")
    #print(result)
    return result

# +
def read_clean_test_expected_results(tab):
    parameters = {
        "file_id": "1CeClWOxaysZztz5V_wxfSvFmd8KzntLc3J67rkhukq4",
        "tab_name": tab,
        "data_range": "B1:E",
        "credentials_json": auth_sup.decode_credentials_json()
    }
    gdse = Google_Sheets_Extractor(parameters,"../test_data/")
    sheets_content = gdse.extract_data()
    google_sheets_df = pd.DataFrame(sheets_content)
    print(google_sheets_df)
    return google_sheets_df


def read_clean_test_data():
    parameters = {
        "file_id": "1CeClWOxaysZztz5V_wxfSvFmd8KzntLc3J67rkhukq4",
        "tab_name": "SampleData",
        "data_range": "A1:E5",
        "credentials_json": auth_sup.decode_credentials_json()
    }
    gdse = Google_Sheets_Extractor(parameters,"../test_data/")
    sheets_content = gdse.extract_data()
    google_sheets_df = pd.DataFrame(sheets_content)
    print(google_sheets_df)
    return google_sheets_df

def write_clean_test_data(data_to_save):
    parameters = {
        "file_id": "1CeClWOxaysZztz5V_wxfSvFmd8KzntLc3J67rkhukq4",
        "tab_name": "Sheet1",
        "data_range": "A1:E5",
        "credentials_json": auth_sup.decode_credentials_json()
    }
    gdse = Google_Sheets_Loader(parameters,"../test_data")
    result = gdse.save_data(data_to_save)
    return result

def write_results_data(data_to_save):
    parameters = {
        "file_id": "1CeClWOxaysZztz5V_wxfSvFmd8KzntLc3J67rkhukq4",
        "tab_name": "Sheet1",
        "data_range": "A3:E",
        "credentials_json": auth_sup.decode_credentials_json()
    }
    gdse = Google_Sheets_Loader(parameters,"../test_data")
    result = gdse.save_data(data_to_save)
    return result


def load_jira_and_google_data_and_reconcile_and_save_results():
    clean_data = read_clean_test_data()
    write_clean_test_data(clean_data.values.tolist())

    rds1 = load_google_data()
    rds2 = load_jira_data()

    rds1[["id"]] = rds1[["id"]].astype(int)
    rds1.index = rds1.index.astype(int)

    rds2[["id"]] = rds2[["id"]].astype(int)
    rds2.index = rds2.index.astype(int)


    result = do_the_reconciliation(rds1, rds2)
    results = write_results_data(result.values.tolist())
    print(result)
    return result
    #write_results_data(result)

    #gsc.reset_sheet_data("Recon Tools Test Data", "write-data-test")
    #gsc.copy_sheet_data("Recon Tools Test Data", "SampleData", "write-data-test")
    #gsc.update_data("Recon Tools Test Data", "write-data-test", "A3", result.to_numpy().tolist() )
    #print("done")


# +
def setup_test_data():
    clean_data = read_clean_test_data()
    write_clean_test_data(clean_data.values.tolist())

#setup_test_data()


# -


def new_e2e_test():
    load_google_data()
    load_jira_data()
    update_data()

# +
#load_jira_data()


# +
#load_google_data()
# -

if __name__ == '__main__':
    load_jira_and_google_data_and_reconcile_and_save_results()
