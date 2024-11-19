import pandas as pd
import os

for year in range(2008, 2014): #years without links and extra preprocessing
    df = pd.read_excel(f"../Data/bills_data_{year}.xlsx")
    df = df.dropna(subset=['Bill Name'])
    
    # Define a function to check and modify the Bill Name
    def process_bill_name(bill_name):
        # Ensure bill_name is a string and strip leading/trailing whitespace
        bill_name = str(bill_name).strip()
        # Check if the Bill Name ends with a 4-digit year
        if bill_name[-4:].isdigit():
            year_part = bill_name[-4:] # Extract the year and remove it from the Bill Name
            bill_name_without_year = bill_name[:-4].strip()  # Remove the year and any trailing space
            return bill_name_without_year
        return None
    
    # Apply the function to the 'Bill Name' column and create a new column with the modified names
    df['Processed Bill Name'] = df['Bill Name'].apply(process_bill_name)

    # Drop rows where 'Processed Bill Name' is None (i.e., no year was found at the end of the Bill Name)
    df = df.dropna(subset=['Processed Bill Name'])

    # Now replace the original 'Bill Name' column with the 'Processed Bill Name' column
    df['Bill Name'] = df['Processed Bill Name']

    # Drop the temporary 'Processed Bill Name' column
    df = df.drop(columns=['Processed Bill Name'])
    df.to_excel(f"../Data/data_{year}.xlsx", index=False)
    print(f"Processed data for {year}.")

for year in range(2015, 2022): #only processing years with links
    df = pd.read_excel(f"../Data/bills_data_{year}.xlsx")
    df = df.dropna(subset=['Bill Name'])
    df.to_excel(f"../Data/data_{year}.xlsx", index=False)


