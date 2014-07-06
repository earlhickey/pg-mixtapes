#!/usr/bin/python
# SMARTMETER agregate data
# @author pG
version = "1.0"

# needed libraries
from datetime import date, timedelta
import sqlite3

# get yesterdays date
ts = date.today() - timedelta(1)
yesterday = ts.strftime('%Y-%m-%d')


# get yesterdays first and last record
conn = sqlite3.connect('/var/db/pg')
c = conn.cursor()
c.execute('''SELECT min("id"),"power_usage_low","power_usage_hi", "power_return_low","power_return_hi","gas_usage","datetime" 
                 FROM energy 
                 WHERE datetime LIKE (? || '%');''', (yesterday,))
first = c.fetchone()
c.execute('''SELECT max("id"),"power_usage_low","power_usage_hi", "power_return_low","power_return_hi","gas_usage","datetime" 
                 FROM energy 
                 WHERE datetime LIKE (? || '%');''', (yesterday,))
last = c.fetchone()

power_usage_low = round(last[1] - first[1], 3)
power_usage_hi = round(last[2] - first[2], 3)
power_return_low = round(last[3] - first[3], 3)
power_return_hi = round(last[4] - first[4], 3)
gas_usage = round(last[5] - first[5], 2)
 
# insert agregated data 
q = '''INSERT INTO "energy_day" ("power_usage_low","power_usage_hi","power_return_low","power_return_hi","gas_usage","date") VALUES (?,?,?,?,?,?)'''
c.execute(q, (power_usage_low, power_usage_hi, power_return_low, power_return_hi, gas_usage, yesterday,))
conn.commit()
c.close()
conn.close()

print (first)
print (last)
