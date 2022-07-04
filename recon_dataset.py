from connectors.googlesheets_connector import GoogleSheets_Connector
from connectors.jira_connector import Jira_Connector
from connectors.base_connector import Base_Connector

import pandas as pd
import json
import numpy as np

class Recon_DataSet:

    def __init__(self, connector = Base_Connector()):
        self.bc = connector
        self.df = None

    def test_first(self):
        return "test_first"

    def set_data(self, cells):
        self.df = pd.DataFrame.from_dict(cells)
        #print(cells)
        #print(self.df)
        return self.df

    def process_data(self, function_in):
        self.df = function_in(self.df)
        return self.df


    def test_two(self):

        return "test_two"



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

        #print("sheetdf")
        #print("")
        #print(sheetdf)
        #print("")

        #print("jiradf")
        #print("")
        #print(jiradf)
        #print("")

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

        # remove header row
        sheetdf = sheetdf.iloc[: , 1:]
        jiradf = jiradf.iloc[: , 1:]


        new_header = sheetdf.iloc[0] #Get the first row for the header
        sheetdf = sheetdf[1:] #Take the data less the header row

        sheetdf.columns = new_header #Set the header row as the df header
        jiradf.columns = new_header

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

        # Notes that didn't quite work...
        #https://moonbooks.org/Articles/How-to-replace-rows-of-a-dataframe-using-rows-of-another-dataframe-based-on-indexes-with-pandas-/
        #https://stackoverflow.com/questions/51394653/update-a-pandas-dataframe-with-data-from-another-dataframe
        #df = sheetdf.combine_first(jiradf).reindex(jiradf.index)

        # Update values where the row is in old and new data sets
        #sheetdf.update(sheetdf[['id']].merge(jiradf, 'left'))

        in_jira =  jiradf.loc[:,"id"].values
        in_sheet = sheetdf.loc[:,"id"].values
        update_rows = np.intersect1d(in_jira, in_sheet)
        for i in update_rows:
            sheetdf.loc[i] = jiradf.loc[i]

        # add new lines to the end
        in_jira =  jiradf.loc[:,"id"].values
        in_sheet = sheetdf.loc[:,"id"].values
        new_rows = np.setdiff1d(in_jira, in_sheet)
        print(in_jira, in_sheet, new_rows)
        print_dataset(sheetdf, "pre result")

        for i in new_rows:
            sheetdf.loc[i] = jiradf.loc[i]

        new_rows = np.setdiff1d(in_jira, in_sheet)
        print(in_jira, in_sheet, new_rows)
        print_dataset(sheetdf, "pre result")


        #dataframe.at[index,'column-name']='new value'
        deleted_rows = np.setdiff1d(in_sheet, in_jira)
        print(deleted_rows)
        for i in deleted_rows:
            sheetdf.loc[i, 'name':] = ""

        print(sheetdf.dtypes)
        print_dataset(sheetdf, "result")

        print(sheetdf.to_numpy().tolist())
        update_cells_test("B1",sheetdf.to_numpy().tolist())


    def test():

        #get_external_data()
        get_local_data()
        #update_cells_test()


        #Class Structure
        test = """
        Connector
        - Connector (JIRAComponent / GoogleSheetsSheet)
        - set_auth_details
        - set_query_details
        - clean_data
        - get_raw_data
        - get_clean_data

        DataProcessorsLibrary
        - cleanJIRAData(dataFrameIn): dataFrameOut

        ReconDatSet
        - PandaDataframe
        - Connector (auth_details, query_details)
        - get_data
        - save_local
        - load_local
        - data_as_dictionary

        Script
        - Create Data set
        - Initialise Auth and Query
        -
        """
