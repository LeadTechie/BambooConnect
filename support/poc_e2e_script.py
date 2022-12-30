

from connectors.googlesheets_connector import GoogleSheets_Connector
#print (connectors.__file__)

from transform.recon_dataset import Recon_DataSet
from connectors.jira_connector import Jira_Connector

import support.authentication_support as auth_sup
import transform.data_translations as dt

import pandas as pd
import numpy as np
import json
import os

#from transform.recon_dataset import Recon_DataSet
#from transform import data_translations

def load_google_data():
    gsc = GoogleSheets_Connector()
    gsc.initialse_auth('CREDENTIALS_JSON')
    #https://stackoverflow.com/questions/394770/override-a-method-at-instance-level
    #gsc.get_clean_data = funcType(gsc, gsc.get_worksheet_values("Recon Tools Test Data", "SampleData")
    #get_my_worksheet_values = gsc.get_worksheet_values
    #gsc.initialse_query(gsc.get_worksheet_values, "Recon Tools Test Data", "SampleData")

    rds1 = Recon_DataSet(gsc)
    gsc.initialse_query(gsc.get_worksheet_values, "Recon Tools Test Data", "SampleData")

    rds1.extract_data()

    rds1.df.to_csv('test_data/sheetdf.csv', encoding='utf-8')
    rds1.transform_function = dt.process_component_sheets_data
    rds1.transform_data()

    return rds1

def load_jira_data():
    jc = Jira_Connector()
    os.environ['RECON_TOOLS_JIRA_EMAIL'] = 'leadtechie@gmail.com'
    jc.initialse_auth('RECON_TOOLS_JIRA_EMAIL', 'RECON_TOOLS_JIRA_TOKEN')
    rds2 = Recon_DataSet(jc)
    jc.initialse_query('https://leadtechie.atlassian.net/rest/api/3/project/TEST/components', dt.flatten_jira_components)

    print(jc.get_raw_data())
    print(jc.get_clean_data())

    rds2.extract_data()
    rds2.df.to_csv('test_data/jiradf.csv', encoding='utf-8')

    rds2.transform_function = dt.process_jira_components_data
    rds2.transform_data()

    #print(rds2.df)
    return rds2

def get_new_data():
    rds2 = load_jira_data()
    rds1 = load_google_data()

    return rds1, rds2

def print_both_datasets(rds1, rds2):
    print("JIRA")
    print(rds2.df)
    print()
    print("Google")
    print(rds1.df)
    print()

def do_the_reconciliation(rds1, rds2):
    print_both_datasets(rds1, rds2)
    result = dt.update_add_delete_data(rds2.df, rds1.df)
    #print("result...")
    #print(result)
    return result

def update_data(result):
    gsc = GoogleSheets_Connector()
    gsc.initialse_auth()
    #gsc.update_cells("Recon Tools Test Data", "SampleData")
    gsc.reset_sheet_data("Recon Tools Test Data", "write-data-test")
    gsc.copy_sheet_data("Recon Tools Test Data", "SampleData", "write-data-test")
    gsc.update_data("Recon Tools Test Data", "write-data-test", "A3", result.to_numpy().tolist() )
    #print("done")

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

if __name__ == '__main__':
    e2e_test()
