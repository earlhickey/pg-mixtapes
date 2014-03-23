#!/usr/bin/python
# SMARTMETER P1 reader
version = "1.0"
import sys
import serial
import time
import sqlite3

# timeout when script takes to long
timeout = time.time() + 30 # 30 sec from now

#Set COM port config
ser = serial.Serial()
ser.baudrate = 9600
ser.bytesize=serial.SEVENBITS
ser.parity=serial.PARITY_NONE
ser.stopbits=serial.STOPBITS_ONE
ser.xonxoff=1
ser.rtscts=0
ser.timeout=20
ser.port="/dev/ttyUSB0"

# start list for data collection
dataList = [None]*7

# Cleanup data
def processData(data):
  # real data is between brackets
   data = data.partition('(')[-1].rpartition(')')[0]
   data = data.replace("*kWh", "")
   data = data.replace("*kW", "")
   data = float(data)
   return data

#Open COM port
try:
  ser.open()
except:
  sys.exit ("Error opening port %s"  % ser.name)      

#Read lines from serial port
while True:
  try:
    data = ser.readline()
    # powerUsageLow
    if data[4:9] == "1.8.1":
      dataList[0] = processData(data)
    # powerUsageHi
    elif data[4:9] == "1.8.2":
      dataList[1] = processData(data) 
    # powerReturnLow
    elif data[4:9] == "2.8.1":
      dataList[2] = processData(data)
    # powerReturnHi
    elif data[4:9] == "2.8.2":
      dataList[3] = processData(data)
    # currentPowerUsage
    elif data[4:9] == "1.7.0":
      currentPowerUsage = processData(data)*1000
      # check for unreal value
      if currentPowerUsage <= "25000":
        dataList[4] = currentPowerUsage
    # currentPowerReturn
    elif data[4:9] == "2.7.0":
      currentPowerReturn = processData(data)*1000
      # check for unreal value
      if currentPowerReturn <= "25000":
        dataList[5] = currentPowerReturn
    # gasUsage
    elif data[0] == "(" and data[10] == ")":
      dataList[6] = processData(data)
    
    # test if all data is collected 
    if None not in dataList or time.time() > timeout:
      break
 
  except:
    sys.exit ("Error can't read port %s" % ser.name )      
    
#Close port and show status
try:
    ser.close()
    except:
    sys.exit ("Error %s. Could not close serial port" % ser.name )

conn = sqlite3.connect('/var/db/pg')
c = conn.cursor()
q = '''INSERT INTO "energy" ("power_usage_low","power_usage_hi","power_return_low","power_return_hi","current_power_usage","current_power_return","gas_usage") VALUES (?,?,?,?,?,?,?)'''
c.execute(q, (dataList))
conn.commit()
c.close()
conn.close()

print (dataList[4])
