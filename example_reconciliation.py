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
    print_dataset(sheetdf, "sheetdf")
    print_dataset(jiradf, "jiradf")


def print_dataset(df, name):
    print(name)
    print("")
    print(df)
    print("")

def get_local_data():
    sheetdf = pd.read_csv('sheetdf.csv', encoding='utf-8')
    jiradf = pd.read_csv('jiradf.csv', encoding='utf-8')

    # remove header row
    sheetdf = sheetdf.iloc[: , 1:]
    jiradf = jiradf.iloc[: , 1:]


    new_header = sheetdf.iloc[0] #Get the first row for the header
    sheetdf = sheetdf[1:] #Take the data less the header row

    sheetdf.columns = new_header #Set the header row as the df header
    jiradf.columns = new_header

    sheetdf['id']=sheetdf['id'].astype('object')
    jiradf['id']=jiradf['id'].astype('object')

    jiradf = jiradf.set_index('id', drop=True)
    sheetdf = sheetdf.set_index('id', drop=True)
    #jiradf.set_index('id', drop=False)
    #sheetdf.set_index('id', drop=False)

    jiradf.index = jiradf.index.astype('object')
    sheetdf.index = sheetdf.index.astype('object')

    sheetdf = sheetdf.drop(columns=['Time Stamp'])
    jiradf = jiradf.drop(columns=['Time Stamp'])

    print("Meta Data")
    print(sheetdf.columns)
    print(jiradf.columns)
    print(sheetdf.dtypes)
    print(jiradf.dtypes)

    print_datasets(sheetdf, jiradf)
    #print(sheetdf.columns)
    #print(jiradf.columns)

    print("changing column type")
    #jiradf.astype({'id': 'object'})
    #pd.to_numeric(jiradf["id"])
    #pd.to_numeric(sheetdf["id"])

    print("sheetdf.info()")
    print(sheetdf.info())

    print("jiradf.info()")
    print(jiradf.info())

    #https://moonbooks.org/Articles/How-to-replace-rows-of-a-dataframe-using-rows-of-another-dataframe-based-on-indexes-with-pandas-/

    #https://stackoverflow.com/questions/51394653/update-a-pandas-dataframe-with-data-from-another-dataframe
    df = sheetdf.combine_first(jiradf).reindex(jiradf.index)

    print_dataset(df, "result")

#get_external_data()
get_local_data()
