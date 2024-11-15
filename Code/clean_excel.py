import pandas as pd


df = pd.read_excel("bills_data_2019.xlsx")
df = df.dropna(subset=['Bill Name'])

# Optional: Save the cleaned DataFrame back to Excel (or perform other operations)
df.to_excel("cleaned_bills_data_2019.xlsx", index=False)
