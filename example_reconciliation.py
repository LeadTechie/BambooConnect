from connectors.googlesheets_connector import GoogleSheets_Connector
from connectors.jira_connector import Jira_Connector
import pandas as pd
import json
import numpy as np

def get_external_data():
    gsc = GoogleSheets_Connector()
    jc = Jira_Connector()
    gsc.initialse_auth()
    jc.initialse_auth()
    all_cells= gsc.get_sheet("Recon Tools Test Data", "Sheet4")
    #jc.get_jira_components_json()
    jira_components = jc.parse_components_with_datetime_stamp()

    sheetdf = pd.DataFrame.from_dict(all_cells)
    jiradf = pd.DataFrame.from_dict(jira_components)

    print("sheetdf")
    print("")
    print(sheetdf)
    print("")

    print("jiradf")
    print("")
    print(jiradf)
    print("")

    sheetdf.to_csv('sheetdf.csv', encoding='utf-8')
    jiradf.to_csv('jiradf.csv', encoding='utf-8')

def update_cells_test(start_cell = 'B1', data=[[1,1],[2,3]]):
    gsc = GoogleSheets_Connector()
    gsc.initialse_auth()
    gsc.update_cells("Recon Tools Test Data","write-data-test",start_cell, data)

def print_datasets(sheetdf, jiradf):
    print_dataset(sheetdf, "sheetdf")
    print_dataset(jiradf, "jiradf")


def print_dataset(df, name):
    print(name)
    print("")
    print(df)
    print("")

# https://stackoverflow.com/questions/15891038/change-column-type-in-pandas
def coerce_df_columns_to_numeric(df, column_list):
    df[column_list] = df[column_list].apply(pd.to_numeric, errors='coerce')

def get_local_data():
    sheetdf = pd.read_csv('sheetdf.csv', encoding='utf-8')
    jiradf = pd.read_csv('jiradf.csv', encoding='utf-8')
