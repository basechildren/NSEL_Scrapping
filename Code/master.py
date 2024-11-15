import pandas as pd
import os

all_data = []

for year in range(2008, 2023):
    file_path = f"../Data/data_{year}.xlsx"
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        all_data.append(df)
    else:
        print(f"File {file_path} does not exist.")

master_df = pd.concat(all_data, ignore_index=True)
master_df = master_df.sort_values(by=['State', 'Year'])
master_df.to_excel("../Data/master_bills_data_2008_2022.xlsx", index=False)
print("Master file created successfully.")
