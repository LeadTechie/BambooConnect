import pandas as pd
import numpy as np
import json
from tabulate import tabulate
import datetime

def test_first():
    #print(pd.read_csv('sheetdf.csv', encoding='utf-8').to_numpy().tolist())

    return "test_first_data_translations"


def make_first_row_header(df):
    new_header = df.iloc[0] #Get the first row for the header
    df.columns = new_header
    df = df[1:] # remove the header row from the data
    return df

def drop_first_row(df):
    df = df.iloc[1: , :]
    return df

def drop_first_column(df):
    df = df.iloc[: , 1:]
    return df

def process_component_sheets_data(df):
    #df = df[1:] # remove first info line
    df = make_first_row_header(df)
    print(df)
    df = standardise_component_data(df)
    return df

def process_component_sheets_data3(df):
    df = df[1:] # remove first info line
    df = make_first_row_header(df)
    print(df)
    df = standardise_component_data(df)
    return df

def process_component_sheets_data2(df):
    df = df[2:] # remove first 2 info lines
    df = make_first_row_header(df)
    print(" DATA...")
    print(df)
    df = standardise_component_data(df)
    return df


def process_jira_components_data(df):
    df.columns = ["Time Stamp","id","name","owner","description"]
    df = standardise_component_data(df)
    return df

# remove empty string ids and convert index colum types to int
def standardise_component_data(df):
    #pd.to_numeric(df['id'], errors='coerce')
    #df = df.replace('NaN',0)
    #df = df.replace('',0)
    #df['id']=df['id'].fillna(0)
    #df['id']=df['id'].astype('int')
    #df.id = df.id.fillna(0)
    #print ("Just id=0")
    #print (df.id == 0)
    #df['First Season'] = (df['First Season'] > 1990).astype(int)
    df = df.set_index('id', drop=False)
    df.index.name = 'index'
    df.index = df.index.fillna(0)
    df.index = df.index.astype('int')
    return df

def print_debug(df, extra_info=""):
    print()
    print(extra_info)
    print(df.dtypes)
    print(df.to_string())
    print(df.to_numpy().tolist())
    print(tabulate(df, headers='keys', tablefmt='psql'))

def flatten_jira_components_with_datetime_stamp(component_json):
    return flatten_jira_components(component_json, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Takes the standard JSON from eg  https://leadtechie.atlassian.net/rest/api/3/project/TEST/components
# and pulls this out to a flat format: time_stampe, id, name, owners, description
def flatten_jira_components(component_json, time_stamp='2022-06-27 22:54:45'):
    results = []
    for component in component_json:
        results.append( [ time_stamp,
            component["id"],
            component["name"],
            component['lead']['displayName'] if 'lead' in component else "<No Owner>",
            component['description'] if 'description' in component else "<No Description>"
            ])
    return results







# https://stackoverflow.com/questions/15891038/change-column-type-in-pandas
def coerce_df_columns_to_numeric(df, column_list):
    df[column_list] = df[column_list].apply(pd.to_numeric, errors='coerce')

def get_local_data():
    sheetdf = pd.read_csv('sheetdf.csv', encoding='utf-8')
    jiradf = pd.read_csv('jiradf.csv', encoding='utf-8')


    sheetdf['id']=sheetdf['id'].astype('int')
    jiradf['id']=jiradf['id'].astype('int')

    jiradf = jiradf.set_index('id', drop=False)
    sheetdf = sheetdf.set_index('id', drop=False)
    #jiradf.set_index('id', drop=False)
    #sheetdf.set_index('id', drop=False)

    #jiradf = jiradf.rename(columns={"id": "myid"})
    #sheetdf = sheetdf.rename(columns={"id": "myid"})
    jiradf.index.name = 'index'
    sheetdf.index.name = 'index'

    jiradf.index.name = 'index'
    sheetdf.index.name = 'index'

    #pd.to_numeric(s)

    jiradf.index = jiradf.index.astype('int')
    sheetdf.index = sheetdf.index.astype('int')

    sheetdf = sheetdf.drop(columns=['Time Stamp'])
    jiradf = jiradf.drop(columns=['Time Stamp'])

    #print("Meta Data")
    #print(sheetdf.columns)
    #print(jiradf.columns)
    #print(sheetdf.dtypes)
    #print(jiradf.dtypes)

    #print_datasets(sheetdf, jiradf)
    #print(sheetdf.columns)
    #print(jiradf.columns)

    print("changing column type")
    #jiradf.astype({'id': 'object'})
    #pd.to_numeric(jiradf["id"])
    #pd.to_numeric(sheetdf["id"])

    #print("sheetdf.info()")
    #print(sheetdf.info())

    #print("jiradf.info()")
    #print(jiradf.info())


def update_add_delete_data(new_data_df, existing_data_df):
    # Notes that didn't quite work...
    #https://moonbooks.org/Articles/How-to-replace-rows-of-a-dataframe-using-rows-of-another-dataframe-based-on-indexes-with-pandas-/
    #https://stackoverflow.com/questions/51394653/update-a-pandas-dataframe-with-data-from-another-dataframe
    #df = sheetdf.combine_first(new_data_df).reindex(jiradf.index)

    # Update values where the row is in old and new data sets
    #sheetdf.update(sheetdf[['id']].merge(jiradf, 'left'))

    #print_debug(existing_data_df, "pre result")

    new_data_ids =  new_data_df.loc[:,"id"].values
    existing_data_ids = existing_data_df.loc[:,"id"].values
    update_rows = np.intersect1d(new_data_ids, existing_data_ids)
    for i in update_rows:
        existing_data_df.loc[i] = new_data_df.loc[i]

    # add new lines to the end
    new_data_ids =  new_data_df.loc[:,"id"].values
    existing_data_ids = existing_data_df.loc[:,"id"].values
    new_rows = np.setdiff1d(new_data_ids, existing_data_ids)
    #print(new_data_ids, existing_data_ids, new_rows)
    #print_debug(existing_data_df, "pre result")

    for i in new_rows:
        existing_data_df.loc[i] = new_data_df.loc[i]

    new_rows = np.setdiff1d(new_data_ids, existing_data_ids)
    #print(new_data_ids, existing_data_ids, new_rows)
    #print_debug(existing_data_df, "pre result")


    #dataframe.at[index,'column-name']='new value'
    deleted_rows = np.setdiff1d(existing_data_ids, new_data_ids)
    #print(deleted_rows)
    for i in deleted_rows:
        existing_data_df.loc[i, 'name':] = ""

    #print(existing_data_df.dtypes)
    #print_debug(existing_data_df, "result")
    return existing_data_df
