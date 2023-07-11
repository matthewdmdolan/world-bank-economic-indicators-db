import requests
import json
import pandas as pd
import sqlite3

# api call v1 - calling for all indicators related to the
URL = "http://api.worldbank.org/v2/topic/3/indicator?format=json&per_page=2000"
r = requests.get(URL)
print(r.status_code)
all_indicators = r.json()
print(all_indicators)
all_indicators = all_indicators[1]

# creates a pretty print output to establish better view of structure
with open('all_indicators.json', 'w') as f:
    json.dump(all_indicators, f, indent=10)

extracted_indicators = [
    {
        'id': item['id'],
        'name': item['name'],
        'unit': item['unit'],
    }
    for item in all_indicators
]
# Create the DataFrame from the extracted data
df_all_indicators = pd.DataFrame(extracted_indicators)
print(df_all_indicators)

# creasting list of all trade indicators
# result gives us 306 rows
df_all_indicators_list = list(df_all_indicators['id'])


# Create a connection to the SQLite database
conn = sqlite3.connect('wdi_trade_indicators.db')

# Write the data to a table called 'my_table' in the SQLite database and ensuring changes occured
df_all_indicators.to_sql('indicators', conn, if_exists='replace')
cursor = conn.cursor()

# Write your SQL query
query = "SELECT * FROM indicators"

# Execute the SQL query
cursor.execute(query)

# Fetch all the rows
rows = cursor.fetchall()

for row in rows:
    print(row)

# Checking datatypes none given
cursor.execute("PRAGMA table_info(indicators)")
rows = (cursor.fetchall())

for row in rows:
    print(row)

# NEED TO ASSIGN DATATYPES

# Don't forget to close the connection
conn.close()
