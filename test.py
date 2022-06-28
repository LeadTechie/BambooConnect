import pandas as pd
import gspread
import base64
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

credentialsb64 = os.getenv('CREDENTIALS_JSON')
print('credentialsb64')
print(credentialsb64)
print('credentialsb64')
credentials = base64.b64decode(credentialsb64)#.decode('ascii')
print(credentials)
print()
json_credentials = json.loads(credentials)
print(json_credentials)
gc = gspread.service_account_from_dict(json_credentials)

sh = gc.open("Recon Tools Test Data")

print(sh.sheet1.get('A1'))
print(sh.sheet1.get('A10'))


#"Recon Tools Test Data", 0, 1, 5, 2, false, true, "../credentials.json", "leadtechie", "TEST", 1, 5
