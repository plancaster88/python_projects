# -*- coding: utf-8 -*-
"""
Created on Thu May 30 10:26:50 2019

@author: a278881
"""

import os 
import re #regular expressions
import pandas as pd
import pyodbc
from datetime import datetime as dt 


query = "select Reason = cast(reason as varchar(max)) + ' '\n\
from planreport_QNXT_LA.dbo.referraltext\n\
where  cast(reason as varchar) <> ''"

#make connection to SQL server
connStr = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server}; \
                            SERVER=SRVQNXTRPTLAPROD; \
                            DATABASE=la_temp; \
                            Trusted_Connection=yes')
#create query object
cursor = connStr.cursor()

#Get all file dates from database and insert into a list 
cursor.execute(query)

notes = []

for i in cursor.fetchall():
    notes.append(i[0])
    
    
bigstring = '' 
for i in notes:
    bigstring += i


def word_count(str):
    counts = dict()
    words = str.split()
    
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    
    return counts

wordcount_dict = word_count(bigstring)
    
index_range = list(range(0,len(wordcount_dict)))

df = pd.DataFrame(list(wordcount_dict.items()), index=index_range, columns=['Word','Count'])   

df_wordcount = df.sort_values(by=['Count'], ascending=False)
    

df.info()
    
