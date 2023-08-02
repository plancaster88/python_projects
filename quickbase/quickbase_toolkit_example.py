import sys 

#set system path to where you are housing the quickbase_toolkit file 
sys.path.append(r'\\winp-sfs-010\McaidNatNDQT\ProvEx Reporting\Phil\Python')

import quickbase_toolkit as qt 

#qt.QuickbaseToolkit.__doc__


apps = {
          'NJ CDM':{'appid':'xxxxxxxxx', 'authorization':'xxxxxx_xxxx_xxxxxxxxxxxxxxxxxxxxxxxxxxx'}
        , 'Quality & Compliance':{'appid':'xxxxxxxxx', 'authorization':'xxxxxx_xxxx_xxxxxxxxxxxxxxxxxxxxxxxxxxx'}
        , 'Par Market Rules' : {'appid':'xxxxxxxxx', 'authorization':'xxxxxx_xxxx_xxxxxxxxxxxxxxxxxxxxxxxxxxx'}
    }




#create quickbase toolkit object 
qb_audit = qt.QuickbaseToolkit(qb_realm_hostname = 'aetna.quickbase.com'
                 , appid = apps['Par Market Rules']['appid']
                 , authorization = apps['Par Market Rules']['authorization']
                 , user_agent = 'Phil Lancaster')

#metadata on app, tables, fields, reports, and relationships
df_qb_app = qb_audit.app_info()
df_qb_tables = qb_audit.table_info()
df_qb_fields = qb_audit.field_info()
df_qb_reports = qb_audit.report_info()
df_qb_relationships = qb_audit.relationship_info()
        

#limit batch_size due to API limits 
df_qb_report_data = qb_audit.get_report(tableid = 'bqz8gv4c3', reportid = 1, batch_size=2000)

df_qb_report_data = pd.DataFrame(df_qb_report_data, dtype = str)

df_qb_report_data = df_qb_report_data[['Record ID#','HealthPlan','Group TIN','Provider NPI', 'Group Name']]




import os 
import pandas as pd 
import pyodbc
import sqlalchemy as sql
from datetime import datetime 


driver = "ODBC Driver 17 for SQL Server"
server = "mbuprodrpt"
database = "pe_temp"
table = "PAR_Market_Rules_Records"
schema = 'qb'

conn2 = sql.create_engine('mssql+pyodbc://{}/{}?driver={}'.format(server,database,driver))#, fast_executemany=True, echo=True)

print(datetime.now()) #start time 

df_qb_report_data.to_sql(name=table
             , schema=schema
             , con = conn2
             , if_exists='replace'
             , index=False
             , chunksize = int(2099/len(df_qb_report_data.columns)) #for whatever reason this is the way to do it... was failing loads prior to this
             , method = 'multi'
             )

print(datetime.now()) #end time 




