import pandas as pd  # type: ignore
import re

# Set of valid years as strings
VALID_YEARS = {str(year) for year in range(2008, 2025)}

# List of state abbreviations and additional prefixes to check
STATE_ABBREVIATIONS = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA",
    "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
    "OR", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]
PREFIXES = ["H", "S", "C"]  # House, Senate, Congress

# Compile regex patterns for validation
state_pattern = re.compile(r'\b(?:' + '|'.join(STATE_ABBREVIATIONS) + r')\b')
prefix_pattern = re.compile(r'\b(?:' + '|'.join(PREFIXES) + r')\s*\d+')  # Allow whitespace between prefix and numbers
date_pattern = re.compile(r'\b\d{2}/\d{2}/\d{4}\b')  # Matches dates in format XX/XX/XXXX

for year in range(2008, 2024):  # Processing years 2008 to 2023
    # Load the Excel file
    df = pd.read_excel(f"../Data/Immigration Legislation Bills/bills_data_{year}.xlsx")
    
    # Drop rows with no 'Bill Name'
    df = df.dropna(subset=['Bill Name'])
    
    # Universal check: Drop rows where 'Bill Name' contains a date
    df = df[~df['Bill Name'].str.contains(date_pattern, na=False)]


    # Process 'Bill Name' to remove trailing valid years (2008-2024)
    def process_bill_name(bill_name):
        # Ensure bill_name is a string and strip leading/trailing whitespace
        bill_name = str(bill_name).strip()
        # Check if the last 4 characters match any valid year
        if len(bill_name) >= 4 and bill_name[-4:] in VALID_YEARS:
            # Remove the year from the Bill Name
            return bill_name[:-4].strip()
        return bill_name  # Return the original name if no valid year is found

    df['Bill Name'] = df['Bill Name'].apply(process_bill_name)
    
    # Drop rows without a bill link and with 'Bill Name' not matching conditions
    if 'Bill Link' in df.columns:
        df['Has Link'] = df['Bill Link'].notna()  # Check if 'Bill Link' exists and is not NaN
    else:
        df['Has Link'] = False  # Default to False if 'Bill Link' is not in the dataset

    # Function to check if a 'Bill Name' is valid
    def is_valid_bill_name(bill_name):
        # Ensure the value is a string
        bill_name = str(bill_name).strip()
        # Check if it contains a state abbreviation or a valid prefix with a number
        return bool(state_pattern.search(bill_name) or prefix_pattern.search(bill_name))

    df['Valid Bill Name'] = df['Bill Name'].apply(is_valid_bill_name)
    
    # Keep rows with either a bill link or a valid bill name
    df = df[(df['Has Link']) | (df['Valid Bill Name'])]

    # Drop temporary columns
    df = df.drop(columns=['Has Link', 'Valid Bill Name'])

    # Save the processed DataFrame to an Excel file
    df.to_excel(f"../Data/Immigration Legislation Bills/data_{year}.xlsx", index=False)

    print(f"Processed data for {year}.")
