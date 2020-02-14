import sqlite3
import os 
import pandas as pd 


db_location = r'C:\Users\c110846\Documents\salesforce_db'

#change to db location directory
os.chdir(db_location)

#connect to db
conn = sqlite3.connect('salesforce.db')


#create a datafrae from a query
df = pd.read_sql_query('''
    SELECT * from sqlite_master where type= "table"
    ''', conn)


#create cursor then execture a sql command 
cursor = conn.cursor()
cursor.execute('drop table event' )


#commit and close
conn.commit()
conn.close()


#Make a db in memory (<3 teh memzorz)
conn = sqlite3.connect(':memory:')

#write the table
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
df.to_sql('df_sqlite_master', conn, index=False, if_exists='replace') #can also append or fail if exists
