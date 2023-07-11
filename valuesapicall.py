import requests
import json
import pandas as pd
import sqlite3

# api call
URL = "http://api.worldbank.org/v2/country/all/indicator/PA.NUS.PPP?format=json&per_page=10000"
r = requests.get(URL)
print(r.status_code)
combined = r.json()
print(combined)

# def get_indicator_data(indicator_codes):
#     data = {}
#     base_url = "http://api.worldbank.org/v2/country/all/indicator/{}?format=json&per_page=2000"
#     for code in indicator_codes:
#         # Format the URL with the current indicator code
#         url = base_url.format(code)
#         # Make the API request
#         response = requests.get(url)
#         # Check the status code of the response
#         if response.status_code == 200:
#             # If successful, save the data
#             data[code] = response.json()
#         else:
#             print(f"Failed to retrieve data for indicator {code}. Status code: {response.status_code}")
#         # Sleep for a while to avoid hitting the rate limit
#         time.sleep(1)
#     return data
#
# # Usage:
# indicator_codes = ["SP.POP.TOTL", "NY.GDP.MKTP.CD", ...]  # replace with your actual indicator codes
# data = get_indicator_data(indicator_codes)


# access first element in list so we can avoid metadata list and access country info
combined = combined[1]

# creates a pretty print output to establish better view of structure
with open('output_combined.json', 'w') as f:
    json.dump(combined, f, indent=10)

extracted_combined = [
    {
        'id': item['indicator']['id'],
        'countryiso3code': item['countryiso3code'],
        'date': item['date'],
        'value': item['value'],
        'unit': item['unit']
    }
    for item in combined
]

# Create the DataFrame from the extracted data
df_combined = pd.DataFrame(extracted_combined)
print(df_combined)

print(df_combined.dtypes)

conn = sqlite3.connect('wdi_trade_indicators.db')

# Write the data to a table called 'my_table' in the SQLite database
df_combined.to_sql('trade_data', conn, if_exists='replace')
cursor = conn.cursor()
query = "SELECT * FROM trade_data"
cursor.execute(query)
rows = cursor.fetchall()

for row in rows:
    print(row)

##Checking datatypes none given
cursor.execute("PRAGMA table_info(trade_data)")
rows = (cursor.fetchall())

for row in rows:
    print(row)

# Don't forget to close the connection
conn.close()
