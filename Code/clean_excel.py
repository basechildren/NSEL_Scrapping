import pandas as pd
import os

for year in range(2008, 2023):
    df = pd.read_excel(f"../Data/bills_data_{year}.xlsx")
    df = df.dropna(subset=['Bill Name'])
    df.to_excel(f"../Data/data_{year}.xlsx", index=False)


