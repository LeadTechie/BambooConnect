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
# #!pip install gspread
import gspread
import sys
import os
import pathlib


os.chdir("..")
try:
    import support.authentication_support as auth_sup
    import transformers.data_translations as dt
    from extractors.google_sheets_extractor import Google_Sheets_Extractor
    from loaders.google_sheets_loader import Google_Sheets_Loader
    from extractors.extractor import Request_Extractor
except Exception as e:
    print(e)    
finally:    
    os.chdir("./samples")



# -

import pandas as pd
import numpy as np
import json
import os

# from transform.recon_dataset import Recon_DataSet
# from transform import data_translations

# +
def load_google_data():
    expected = [['TestComponent1'],
                ['TestComponent2'],
                ['TestComponent3']]

    parameters = {
        "file_id": "1CeClWOxaysZztz5V_wxfSvFmd8KzntLc3J67rkhukq4",
        "tab_name": "sheet1",
        "data_range": "A1:E",
        "credentials_json": auth_sup.decode_credentials_json()
    }
    gdse = Google_Sheets_Extractor(parameters,"../test_data/")
    sheets_content = gdse.extract_data()
    google_sheets_df = pd.DataFrame(sheets_content)
    google_sheets_df_updated = dt.process_component_sheets_data(google_sheets_df)
    print(google_sheets_df_updated)
    return google_sheets_df_updated

load_google_data()


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

def get_new_data():
    rds2 = load_jira_data()
    rds1 = load_google_data()

    return rds1, rds2

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
def read_clean_test_data():
    expected = [['TestComponent1'],
                ['TestComponent2'],
                ['TestComponent3']]

    parameters = {
        "file_id": "1CeClWOxaysZztz5V_wxfSvFmd8KzntLc3J67rkhukq4",
        "tab_name": "SampleData",
        "data_range": "A2:E5",
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
        "data_range": "A1:E4",
        "credentials_json": auth_sup.decode_credentials_json()
    }
    gdse = Google_Sheets_Loader(parameters,"../test_data")
    result = gdse.save_data(data_to_save)
    return result

def write_results_data(data_to_save):
    parameters = {
        "file_id": "1CeClWOxaysZztz5V_wxfSvFmd8KzntLc3J67rkhukq4",
        "tab_name": "Sheet1",
        "data_range": "A1:E",
        "credentials_json": auth_sup.decode_credentials_json()
    }
    gdse = Google_Sheets_Loader(parameters,"../test_data")
    result = gdse.save_data(data_to_save)
    return result


def update_data(result):
    clean_data = read_clean_test_data()
    write_clean_test_data(clean_data.values.tolist())
    print(result)
    
    rds1, rds2 = get_new_data()
    result = do_the_reconciliation(rds1, rds2)
    print(result)
    #write_results_data(result)
    
    #gsc.reset_sheet_data("Recon Tools Test Data", "write-data-test")
    #gsc.copy_sheet_data("Recon Tools Test Data", "SampleData", "write-data-test")
    #gsc.update_data("Recon Tools Test Data", "write-data-test", "A3", result.to_numpy().tolist() )
    #print("done")
    
update_data(None)    


# -

def get_local_data():
    sheetdf = pd.read_csv('test_data/sheetdf.csv', encoding='utf-8')
    rds1 = Recon_DataSet()
    rds1.df = sheetdf

    rds2 = Recon_DataSet()
    rds2.df = pd.read_csv('test_data/jiradf.csv', encoding='utf-8')

    return rds1, rds2

def e2e_test():
    rdss = get_new_data()
    result = do_the_reconciliation(rdss[0], rdss[1])
    update_data(result);


    print("get local data")
    rdss = get_local_data()
    print_both_datasets(rdss[0], rdss[1])
    # re-opening csvs that were created by panda seem to have extra first column
    rdss[0].transform_data_with_function(dt.drop_first_column)
    rdss[0].transform_data_with_function(dt.process_component_sheets_data)
    rdss[1].transform_data_with_function(dt.drop_first_column)
    rdss[1].transform_data_with_function(dt.process_jira_components_data)
    result = do_the_reconciliation(rdss[0], rdss[1])

    update_data(result);



def new_e2e_test():
    load_google_data()
    load_jira_data()    


if __name__ == '__main__':
    new_e2e_test()




