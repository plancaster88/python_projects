'''
CREATE TABLE [pe].[PythonScriptScheduler](
	[FileID] [int] IDENTITY(1,1) NOT NULL,
	[FileName] [varchar](max) NULL,
	[FilePath] [varchar](max) NULL,
	[RunFreq] [varchar](10) NULL,
	[RunHour] [int] NULL,
	[RunPeriod] [varchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[FileID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

FileID	FileName	FilePath	RunFreq	RunHour	RunPeriod
9	par_market_rules.py	\\winp-sfs-010\McaidNatNDQT\ProvEx Reporting\Phil\Python\ETL Processes\par market rules	D	8	0
10	delegated_providers.py	\\winp-sfs-010\McaidNatNDQT\ProvEx Reporting\Phil\Python\ETL Processes\delegated providers	D	7	0
11	medicaid_pcr_consolidation.py	\\winp-sfs-010\McaidNatNDQT\ProvEx Reporting\Phil\Python\ETL Processes\Medicaid PCR Consolidation	D	6	0
12	credentialing_scorecard.py	\\winp-sfs-010\McaidNatNDQT\ProvEx Reporting\Phil\Python\ETL Processes\credentialing_scorecard	W	5	2
13	ky_vbs_group_files.py	\\winp-sfs-010\McaidNatNDQT\ProvEx Reporting\Phil\Python\KY VBS Group Files	M	15	13,14,15
16	oh_rise_new_providers.py	\\winp-sfs-010\McaidNatNDQT\ProvEx Reporting\Phil\Python\OH Rise Providers	W	8	2
18	oh_rise.py	\\winp-sfs-010\McaidNatNDQT\ProvEx Reporting\Phil\Python\ETL Processes\OH Rise	D	10	0
19	pds_audit_qb.py	\\winp-sfs-010\McaidNatNDQT\ProvEx Reporting\Phil\Python\ETL Processes\pds_scorecard	D	9	0
21	recred_due.py	\\winp-sfs-010\McaidNatNDQT\ProvEx Reporting\Phil\Python\ETL Processes\Recred Due	M	11	1,2,3,4,5,6,7
'''

import pandas as pd
import pyodbc
import sqlalchemy as sql
from datetime import datetime

#create connection to SQL Server 
conn= pyodbc.connect('DRIVER={SQL Server}; \
                            SERVER=MBUPRODRPT; \
                            DATABASE=pe_temp; \
                            Trusted_Connection=yes')

cursor = conn.cursor()

#Get all records from schedule table
sql = 'select * from pe_temp.pe.PythonScriptScheduler'

df = pd.read_sql(sql,conn)

#get current time 
current_time = datetime.now()
current_hour = int(current_time.strftime("%H"))
current_dayofmonth = int(current_time.strftime("%d"))
current_dayofweek = int(current_time.strftime("%w")) + 1


df['RunFreq'] = df['RunFreq'].apply(lambda x: x.upper())

#Get anything run hourly 
df_keep_hourly = df[df['RunFreq'] == 'H']

#Get anything run daily in current hour 
df_keep_daily = df[(df['RunFreq'] == 'D') & (df['RunHour'] == current_hour)]


#Get anything run weekly in current day and hour 
df_keep_weekly = df[(df['RunFreq'] == 'W') & (df['RunHour'] == current_hour) & (df['RunPeriod'] == current_dayofweek)]

#Get anything run moenthly in current day and hour 
df_keep_monthly = df[(df['RunFreq'] == 'M') & (df['RunHour'] == current_hour) & (df['RunPeriod'] == current_dayofmonth)]


#combine all files that need to be run
df_keep = pd.concat([df_keep_hourly, df_keep_daily, df_keep_weekly, df_keep_monthly])


#loop through all scripts in dataframe and run them 
for index, row in df_keep.iterrows():
    
    starttime = datetime.now()
    
    print('Start Script: ' + row['FileName'] + ' ' + str(datetime.now()))
    py_file = row['FilePath'] + '\\'+ row['FileName']
    
    #executes python script
    exec(open(py_file).read()) 
         
    cursor.execute('''
        INSERT INTO  pe_temp.pe.PythonScriptRuns  (FilePath, FileName, LoadStart, LoadEnd)
        VALUES
        (?,?,?,?)
        ''', (row['FilePath'], row['FileName'], starttime, datetime.now())
        )
    
    print('End Script: ' + row['FileName'] + ' ' + str(datetime.now()))

    conn.commit()


conn.close()


