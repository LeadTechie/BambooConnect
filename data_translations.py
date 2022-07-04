import pandas as pd
import numpy as np
import json
from tabulate import tabulate

def test_first():
    #print(pd.read_csv('sheetdf.csv', encoding='utf-8').to_numpy().tolist())

    return "test_first_data_translations"


def make_first_row_header(df):
    new_header = df.iloc[0] #Get the first row for the header
    df.columns = new_header
    df = df[1:] # remove the header row from the data
    return df

def process_component_sheets_data(df):
    df = df[1:] # remove first info line
    df = make_first_row_header(df)
    df = standardise_component_data(df)
    return df

def process_jira_components_data(df):
    df.columns = ["Time Stamp","id","name","owner","description"]
    df = standardise_component_data(df)
    return df

def standardise_component_data(df):
    df['id']=df['id'].astype('int')
    df = df.set_index('id', drop=False)
    df.index.name = 'index'
    df.index = df.index.astype('int')
    return df

def print_debug(df, extra_info=""):
    print()
    print(extra_info)
    print(df.dtypes)
    print(df.to_string())
    print(df.to_numpy().tolist())
    print(tabulate(df, headers='keys', tablefmt='psql'))


def to_remove():
    #df = df.iloc[: , 1:] # removes the first column
    sheetdf = sheetdf[1:] #Take the data less the header row

    sheetdf.columns = new_header #Set the header row as the df header


    jiradf = jiradf.iloc[: , 1:]


    new_header = sheetdf.iloc[0] #Get the first row for the header
    sheetdf = sheetdf[1:] #Take the data less the header row

    sheetdf.columns = new_header #Set the header row as the df header
    jiradf.columns = new_header


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

    print_datasets(sheetdf, jiradf)
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

    new_data_ids =  new_data_df.loc[:,"id"].values
    existing_data_ids = existing_data_df.loc[:,"id"].values
    update_rows = np.intersect1d(new_data_ids, existing_data_ids)
    for i in update_rows:
        existing_data_df.loc[i] = new_data_df.loc[i]

    # add new lines to the end
    new_data_ids =  new_data_df.loc[:,"id"].values
    existing_data_ids = existing_data_df.loc[:,"id"].values
    new_rows = np.setdiff1d(new_data_ids, existing_data_ids)
    print(new_data_ids, existing_data_ids, new_rows)
    print_debug(existing_data_df, "pre result")

    for i in new_rows:
        existing_data_df.loc[i] = new_data_df.loc[i]

    new_rows = np.setdiff1d(new_data_ids, existing_data_ids)
    print(new_data_ids, existing_data_ids, new_rows)
    print_debug(existing_data_df, "pre result")


    #dataframe.at[index,'column-name']='new value'
    deleted_rows = np.setdiff1d(existing_data_ids, new_data_ids)
    print(deleted_rows)
    for i in deleted_rows:
        existing_data_df.loc[i, 'name':] = ""

    print(existing_data_df.dtypes)
    print_debug(existing_data_df, "result")
    return existing_data_df
