import requests
import json
import pandas as pd
import sqlite3

conn = sqlite3.connect('wdi_trade_indicators.db')

# Write the data to a table called 'my_table' in the SQLite database
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