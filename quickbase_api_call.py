
import json
import requests
import pandas as pd 


def union_df(maindf, tempdf):
    if  maindf.empty:
        maindf = tempdf
    else:
        maindf = pd.concat([maindf, tempdf]) #union all in sql...basically
    return maindf



qb_df = pd.DataFrame()
skip = 0 
top = 1000
records = 1

while records != 0:
    #API call 
    headers = {
      	'QB-Realm-Hostname': 'aetna.quickbase.com',
    	'User-Agent': '{User-Agent}',
    	'Authorization': 'QB-USER-TOKEN xxxxxx_xxxx_xxxxxxxxxxxxxxxxxxxxxxxxxxx'
    }
    
    params = {
      	'tableId': 'xxxxxxxxx' 
        , 'top': top
        , 'skip': skip
    }
    
    r = requests.post(
    'https://api.quickbase.com/v1/reports/1/run', #see QB REST API Documentation 
    params = params, 
    headers = headers,
    proxies={'https': None}
    )
    
    #get the data
    data = r.json()['data']
    
    #once this hits 0 it ends loop 
    records = len(data)
    
    if records != 0: 
        #gets to the data level
        data_step_1 = [list(x.values()) for x in data]      
        data_step_2 = [[list(y.values())[0] for y in x] for x in data_step_1]  
        
        #gets column numbers
        column_nums = list(data[0].keys())
        
        #create dataframe
        df = pd.DataFrame(data_step_2, columns = column_nums)
        
        #combine the dataframes sql union style 
        qb_df = union_df(qb_df, df)
        
        #report where you are in your load
        skip += top
        print(str(skip - top + len(data)) +  ' rows loaded')


#rename columns 
fields = r.json()['fields']

column_names = {} #empty dictionary to add 
for i in [[str(x['id']) ,  x['label'] ]for x in fields]:
    column_names[i[0]] = i[1]


qb_df = qb_df.rename(columns=column_names)
