import pandas as pd
import json
import os

file = "data1.csv"

# Reading CSV
df = pd.read_csv(file)

# Changing Delimiter
symbol = "|"
pd.read_csv(file, sep = symbol)

output = df.sort_values(by = "a")
print(output)

#def jira_googlesheets_reconcile_and_update(
#sheet_name, tab_number, sheet_col_start, sheet_col_end, row_offset,

#copy_flag=false, write_change_log=false, google_credentials_file, company_url_base, project, jira_col_start, jira_col_end)
#"Recon Tools Test Data", 0, 1, 5, 2, false, true, "../credentials.json", "leadtechie", "TEST", 1, 5
