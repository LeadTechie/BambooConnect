import pandas as pd
import numpy as np
import json
import os
from connectors.googlesheets_connector import GoogleSheets_Connector
from connectors.jira_connector import Jira_Connector

import data_translations as dt

from recon_dataset import Recon_DataSet

def load_google_data():
    gsc = GoogleSheets_Connector()
    gsc.initialse_auth()
    #https://stackoverflow.com/questions/394770/override-a-method-at-instance-level
    #gsc.get_clean_data = funcType(gsc, gsc.get_worksheet_values("Recon Tools Test Data", "SampleData")

    rds1 = Recon_DataSet(gsc)
    all_cells= gsc.get_raw_data("Recon Tools Test Data", "SampleData")
    rds1.set_data(all_cells)
    rds1.process_data(dt.process_component_sheets_data)
    #print(rds1.df)

    #print(rds1.test_first())
    #print(rds1.df)
    return rds1

def load_jira_data():
    jc = Jira_Connector()
    os.environ['RECON_TOOLS_JIRA_EMAIL'] = 'leadtechie@gmail.com'
    os.environ['RECON_TOOLS_JIRA_SERVER'] = 'https://leadtechie.atlassian.net'
    rds2 = Recon_DataSet(jc)
    jc.initialse_auth()
    full_components_from_jira = jc.get_clean_data()
    rds2.set_data(full_components_from_jira)
    rds2.process_data(dt.process_jira_components_data)
    #print(rds2.df)
    return rds2

def get_new_data():
    rds1 = load_google_data()
    rds2 = load_jira_data()

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

result = get_new_data()
update_data(result);
