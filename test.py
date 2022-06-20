import pandas as pd

file = "data1.csv"

# Reading CSV
df = pd.read_csv(file)

# Changing Delimiter
symbol = "|"
pd.read_csv(file, sep = symbol)

output = df.sort_values(by = "a")
print(output)
