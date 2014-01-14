#!/usr/bin/env python

import sys
import commands
import argparse
import csv
import xlwt
from xlwt import *

# arguments
parser = argparse.ArgumentParser()
parser.add_argument("export", help="What do you want to export?")
args = parser.parse_args()
#print(args.export)

# name/file, query, db, user, pw, to
exports = [
  ['tblName1', 'SELECT field1, field2, field3 FROM tblName1 WHERE field1 = \'bla bla\';', 'dbName1', 'userName', 'passwd', 'name@gmail.com,name2@gmail.com'],
  ['tblName2','SELECT * FROM tblName2;','dbName2', 'userName', 'passwd', 'name@gmail.com,name2@gmail.com']]

for export in exports:
  if args.export == export[0]:
    # export 
    print commands.getstatusoutput('/usr/bin/mysql -B -u' + export[3] + ' -p' + export[4] + ' -h localhost -e "' + export[1] + '" ' + export[2] + ' > /tmp/' + export[0] + '.csv')
    # csv to xls
    f=open('/tmp/' + export[0] + '.csv', 'rb')
    g=csv.reader ((f), delimiter="	")
    wbk=xlwt.Workbook()
    sheet = wbk.add_sheet("Sheet 1")
    for rowi, row in enumerate(g):
      for coli, value in enumerate(row):
        sheet.write(rowi,coli,value.decode('utf8')) 
    wbk.save('/tmp/' + export[0] + '.xls') 
    # email file
    print commands.getstatusoutput('/usr/bin/mpack -s ' + export[0] + ' /tmp/' + export[0] + '.xls ' + export[5])
