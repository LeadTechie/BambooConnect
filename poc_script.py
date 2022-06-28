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


#"Recon Tools Test Data", 0, 1, 5, 2, false, true, "../credentials.json", "leadtechie", "TEST", 1, 5
