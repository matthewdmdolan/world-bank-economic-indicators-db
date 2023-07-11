import requests
import json
import pandas as pd
import sqlite3

# api call
URL = "http://api.worldbank.org/v2/country/all?format=json&per_page=2000"
r = requests.get(URL)
print(r.status_code)
countries = r.json()
print(countries)

# access second element in list so we can avoid metadata list and access country info
countries = countries[1]

# creates a pretty print output to establish better view of structure
with open('output_countries.json', 'w') as f:
    json.dump(countries, f, indent=10)

# loops through json to extract fields defined below
extracted_countries = [
    {
        'id': item['id'],
        'iso2Code': item['iso2Code'],
        'name': item['name'],
        'capitalCity': item['capitalCity'],
        'longitude': item['longitude'],
        'latitude': item['latitude'],
        'incomeLevel_id': item['incomeLevel']['id'],
        'incomeLevel_iso2code': item['incomeLevel']['iso2code'],
        'incomeLevel_value': item['incomeLevel']['value'],
        'lendingType': item['lendingType']['id']
    }
    for item in countries
]

# Create the DataFrame from the extracted data
df = pd.DataFrame(extracted_countries)
print(df)

print(df.columns)

#normalising income level data
df_income_level = df[['incomeLevel_id', 'incomeLevel_iso2code', 'incomeLevel_value']]
print(df_income_level)


#normalising country level data
df_country = df[['id', 'iso2Code', 'name', 'capitalCity', 'longitude', 'latitude',  'lendingType']]
print(df_country)


# Create a connection to the SQLite database
conn = sqlite3.connect('wdi_trade_indicators.db')

# Write the data to a table called 'my_table' in the SQLite database
df_country.to_sql('countries', conn, if_exists='replace')
cursor = conn.cursor()
query = "SELECT * FROM countries"
cursor.execute(query)
rows = cursor.fetchall()
for row in rows:
    print(row)

# Checking datatypes none given
cursor.execute("PRAGMA table_info(countries)")
rows = (cursor.fetchall())

for row in rows:
    print(row)




df_income_level.to_sql('incomelevel', conn, if_exists='replace')
cursor = conn.cursor()
query = "SELECT * FROM incomelevel"
cursor.execute(query)
rows = cursor.fetchall()
for row in rows:
    print(row)

# Checking datatypes none given
cursor.execute("PRAGMA table_info(countries)")
rows = (cursor.fetchall())

for row in rows:
    print(row)


# NEED TO ASSIGN DATATYPES


# Don't forget to close the connection
#conn.close()