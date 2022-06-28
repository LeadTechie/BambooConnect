from connectors.googlesheets_connector import GoogleSheets_Connector
from connectors.jira_connector import Jira_Connector
import pandas as pd
import json


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

def print_datasets(sheetdf, jiradf):
    print("sheetdf")
    print("")
    print(sheetdf)
    print("")

def print_dataset(df, name):
    print(name)
    print("")
    print(df)
    print("")

def get_local_data():
    sheetdf = pd.read_csv('sheetdf.csv', encoding='utf-8')
    jiradf = pd.read_csv('jiradf.csv', encoding='utf-8')

    new_header = sheetdf.iloc[0] #Get the first row for the header
    sheetdf = sheetdf[1:] #Take the data less the header row
    sheetdf.columns = new_header #Set the header row as the df header

    jiradf.columns = new_header

    #Find Rows in DF1 Which Are Not Available in DF2
    #https://kanoki.org/2019/07/04/pandas-difference-between-two-dataframes/
    #df = df1.merge(df2, how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']

    #df = sheetdf.merge(jiradf, on=['id'].astype(int), how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']

    print_datasets(sheetdf, jiradf)

    #print_dataset(df, "result")


get_local_data()
