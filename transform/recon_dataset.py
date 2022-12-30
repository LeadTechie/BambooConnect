from connectors.googlesheets_connector import GoogleSheets_Connector
from connectors.jira_connector import Jira_Connector
from connectors.base_connector import Base_Connector

import pandas as pd
import json
import numpy as np

class Recon_DataSet():

    def __init__(self, connector = Base_Connector(), df_in = None):
        self.bc = connector # A Py Recon Tools connector, eg JIRA, GoogleSheets Connector
        self.df = df_in #dataframe that stores the data via Pandas dataframe
        self.transform_function = None

    def test_first(self):
        return "test_first"

    def extract_data(self):
        cells = self.bc.get_clean_data()
        self.df = pd.DataFrame.from_dict(cells)
        return self.df

    def transform_data(self):
        self.df = self.transform_function(self.df)
        return self.df

    def transform_data_with_function(self, function_in):
        self.df = function_in(self.df)
        return self.df
