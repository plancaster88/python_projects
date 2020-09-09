

import pyodbc
import pandas as pd
import sqlalchemy as sql
import sys 

DRIVER = "ODBC Driver 17 for SQL Server"
DSN = "mbuprodrpt"
DB = "pe_temp"
TABLE = "temptest"
SCHEMA = 'temp'



conn_sqlalchemy = sql.create_engine(f"mssql+pyodbc://{DSN}/{DB}?driver={DRIVER}")

conn_executemany = sql.create_engine(f"mssql+pyodbc://{DSN}/{DB}?driver={DRIVER}"
                                     , fast_executemany=True)


print("DataFrame is", round(sys.getsizeof(qb_df) / 1024 ** 2, 1), "MB")


qb_df.to_sql(name=TABLE
             , schema=SCHEMA
             , con = conn_sqlalchemy
             , if_exists='replace'
             , index=False
             , chunksize = int(2099/len(qb_df.columns)) #for whatever reason this is the way to do it... was failing loads prior to this
             , method = 'multi'
             )
