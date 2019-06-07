# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 13:03:14 2019

@author: A278881
"""

import os 
import re #regular expressions
import pandas as pd
import pyodbc
from datetime import datetime as dt 

file_keyword = 'MMIS_FQHC_AND_RHC_'
file_extension = 'txt'

#r in front is a raw string... 
path = r'\\midp-sfs-006\aetnabttrhlthlastfls'


#change to the directory 
os.chdir(path)

#regular expression to find matching files

files = [f for f in os.listdir(path) if re.findall('^{}.*[.]{}$'\
         .format(file_keyword.lower(), file_extension.lower()),f.lower())] 
#make format() and regex findall() case insensitive

#regex guide https://www.w3schools.com/python/python_regex.asp
# ^ is starts with
# {} is a placeholder for .format()
# . is any 1 character
# * is any # of occurences (including 0) of previous character (.* = % in SQL)
# $ is ends with
# [] is virtually the same as SQL regex

#sort list to get most recent file  
files.sort(reverse=True) #sort descending

#get first file in list 
#files[0]

df = pd.read_csv(files[0], skiprows=2, sep = '\t')

df.columns = [i.strip() for i in list(df.columns.values)]

df.drop([''], axis=1, inplace=True)

#get file date
file_date = files[0].lower().replace('.' + file_extension, '')[-8:]

#create file date column
df['FileDate'] = file_date

#Use this method when coding datetime from YYYYMMDD.
df['RATE EFF'] = pd.to_datetime(df['RATE EFF'], format='%Y%m%d')
df['FileDate'] = pd.to_datetime(df['FileDate'], format='%Y%m%d') 
df['EFF DTE'] = pd.to_datetime(df['EFF DTE'], format='%Y%m%d') 

#fill all values for END DTE with NULL since they are always empty
df['END DTE'] = None

#make connection to SQL server
connStr = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server}; \
                            SERVER=SRVQNXTRPTLAPROD; \
                            DATABASE=la_temp; \
                            Trusted_Connection=yes')
#create query object
cursor = connStr.cursor()

#Get all file dates from database and insert into a list 
cursor.execute('select distinct convert(char(8), FileDate,112) \
               from dbo.FQHCRHCFeeSched')

filedates_in_sqlserver = []

for i in cursor.fetchall():
    filedates_in_sqlserver.append(i[0])
    
#get current time
run_datetime = dt.now().strftime('%Y-%m-%d %H:%M:00')    

#Put all records into a list (doing this way is fairlyquick)
records = []

for index,row in df.iterrows():
    records.append(list([row[0],row[1].strip(),row[2].strip()
               ,row[3].strip(),row[4],row[5],row[6],row[7]
               ,row[8].strftime('%Y-%m-%d'),row[9],row[10]
               ,row[11],row[12],row[13].strftime('%Y-%m-%d')
               ,row[14].strftime('%Y-%m-%d'),run_datetime]))
    

run_outcome = ''

if file_date not in filedates_in_sqlserver:
    #Turn list into a string for bulk insert into database
    records_to_string = ''
    
    #loop to process in batches
    for index, list_item in enumerate(records):
        #create batch of 100 records
        records_to_string += 'INSERT INTO dbo.FQHCRHCFeeSched values (' \
            +  str(list_item)[1:-1] + ')' 
       #upload batch... sql stops after 1000ish records get uploaded at a time
        if index % 100 == 0:
            records_to_string = records_to_string.replace(', None,', ', NULL,')
            cursor.execute(records_to_string) 
            #reset bulk upload string
            records_to_string = ''      
    
    #insert any left over records 
    records_to_string = records_to_string.replace(', None,', ', NULL,')
    cursor.execute(records_to_string) 
    run_outcome = 'Data loaded to la_temp'
elif file_date in filedates_in_sqlserver:
    run_outcome = 'Data loaded to la_temp'
else:
    run_outcome = 'Data load unsuccessful'
    
   
   
#Get count of records uploaded to sql
cursor.execute('select count(*) from la_temp.dbo.FQHCRHCFeeSched where\
               convert(char(8), FileDate, 112) =' + file_date)

records_in_sql = []

for i in cursor.fetchall():
    records_in_sql.append(i[0])    


connStr.commit() #commit and close connection
cursor.close()
connStr.close()  
  
    
#Load Outcome into PBI
outcome = pd.DataFrame( [[file_keyword + file_date + '.' + file_extension
    , df['FileDate'][0].strftime('%Y-%m-%d'), run_datetime, run_outcome
    , df.shape[0], records_in_sql[0]]]
    , columns=['File', 'File Date','Run Time','Outcome'
               , 'Records in File' ,'Records in SQL'])

outcome
