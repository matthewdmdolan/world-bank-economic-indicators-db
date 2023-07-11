import requests
import json
import pandas as pd
import sqlite3
import time
from indicatorsapicall import df_all_indicators_list

# API base URL
API_BASE_URL = "http://api.worldbank.org/v2/country/all/indicator"

# List of indicator codes
df_all_indicators_list = df_all_indicators_list  # Replace with your full list of indicator codes

# Container for combined data
combined_data = []

# Iterate over indicator codes
for indicator_code in df_all_indicators_list:
    # API call for each indicator
    url = f"{API_BASE_URL}/{indicator_code}?format=json&per_page=10000"
    response = requests.get(url)
    print(response.status_code)

    # Extract data from the response if available
    if response.status_code == 200:
        data = response.json()
        if len(data) > 1:
            data = data[1]  # Skip metadata

            # Append to combined data
            combined_data.extend(data)

    # Pause for a while before making the next API call
    time.sleep(1)  # Adjust the sleep period as needed

# Create a pretty print output to establish a better view of the structure
with open('output_combined.json', 'w') as f:
    json.dump(combined_data, f, indent=10)

# Extract relevant fields from combined data
extracted_combined = [
    {
        'id': item['indicator']['id'],
        'countryiso3code': item['countryiso3code'],
        'date': item['date'],
        'value': item['value'],
        'unit': item['unit']
    }
    for item in combined_data
]

# Create the DataFrame from the extracted data
df_combined = pd.DataFrame(extracted_combined)
print(df_combined)

# Connect to the SQLite database
conn = sqlite3.connect('wdi_trade_indicators.db')

# Write the data to a table called 'values' in the SQLite database
df_combined.to_sql('values', conn, if_exists='replace')

# Query the table to verify the data
cursor = conn.cursor()
query = "SELECT * FROM values"
cursor.execute(query)
rows = cursor.fetchall()

for row in rows:
    print(row)

# Check the data types of the table columns
cursor.execute("PRAGMA table_info(values)")
rows = cursor.fetchall()

for row in rows:
    print(row)

# Close the connection
conn.close()
