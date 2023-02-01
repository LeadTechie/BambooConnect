import os
from connectors.jira_obss_plugin_connector import Jira_OBSS_Plugin_Connector

from transform.recon_dataset import Recon_DataSet
import support.poc_e2e_script as e2e

jobss = Jira_OBSS_Plugin_Connector()
print(jobss.quicktest())

obss_query_string = os.getenv("OBSS_FULL_URL")

jobss.initialse_auth("OBSS_TISJWT", obss_query_string)

rds = Recon_DataSet(jobss)
df = rds.extract_data()
print(df.columns)
print(df)
