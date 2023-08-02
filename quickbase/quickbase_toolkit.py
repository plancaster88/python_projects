import pandas as pd 
import requests
import getpass
import base64


class QuickbaseToolkit:
    
    '''
    https://developer.quickbase.com/operation/getApp for info on arguments
    args - (qb_realm_hostname, appid, authorization, user_agent='User Agent Not Supplied')
    '''
   
    def __init__(self, qb_realm_hostname, appid, authorization
                 , user_agent='User Agent Not Supplied'):
        
        self.qb_realm_hostname = qb_realm_hostname
        self.appid = appid
        self.authorization = 'QB-USER-TOKEN ' + authorization
        self.user_agent = user_agent
        
        
        
        #this is where we pass credentials in 
        self.proxies = {'https' : 'http://' + getpass.getuser() + ':' 
            + str(base64.b64decode(open(r'C:\config\config.txt', "r").read()))[2:-1] 
            + '@proxy:9119'}
        
        
        
        self.headers = {
          	'QB-Realm-Hostname': qb_realm_hostname
        	, 'User-Agent': user_agent
        	, 'Authorization': 'QB-USER-TOKEN ' + authorization
        }
        
           
    def app_info(self): 
        r = requests.get(
            'https://api.quickbase.com/v1/apps/{}'.format(self.appid)
            , proxies = self.proxies
            , headers = self.headers
        )
        
        return pd.DataFrame(r.json(), index=[0])

    def table_info(self): 
        params = {
          	'appId': self.appid
        }
        r = requests.get(
            'https://api.quickbase.com/v1/tables'
            , proxies = self.proxies
            , params = params
            , headers = self.headers
        )        
        
        table_df = pd.DataFrame(r.json())
        table_df['appId'] = self.appid
        table_df['appName'] = self.app_info()['name'][0]
        
        
        return table_df

    def field_info(self): 

        
        table_df = self.table_info()
        
        app_tables = list(zip(table_df['id'], table_df['name']))
        
        field_df_list = [] 
        
        for table in app_tables:
            
            params = {
              	'tableId': table[0]
                  , 'includeFieldPerms': 'true'
            }
            r = requests.get(
                'https://api.quickbase.com/v1/fields' 
                , params = params
                , proxies = self.proxies
                , headers = self.headers
            )
                   
            field_df = pd.DataFrame(r.json())
            
            field_df['tableId'] = table[0]
            field_df['tableName'] = table[1]
            field_df['appId'] = self.appid
            field_df['appName'] = self.app_info()['name'][0]
            
            field_df_list.append(field_df)    
            field_df_all = pd.concat(field_df_list)

        return field_df_all
    
    def report_info(self): 
           
        table_df = self.table_info()
        
        app_tables = list(zip(table_df['id'], table_df['name']))
        
        report_df_list = [] 
        
        for table in app_tables:      
        
            params = {
              	'tableId': table[0]
            }
            r = requests.get(
                'https://api.quickbase.com/v1/reports'
                , params = params
                , proxies = self.proxies
                , headers = self.headers
            )
                       
            report_df = pd.DataFrame(r.json())
            
            report_df['tableId'] = table[0]
            report_df['tableName'] = table[1]
            report_df['appId'] = self.appid
            report_df['appName'] = self.app_info()['name'][0]
            
            report_df_list.append(report_df)       
            report_df_all = pd.concat(report_df_list)

        return report_df_all          
            
            
    def relationship_info(self): 
           
        table_df = self.table_info()
        
        app_tables = list(zip(table_df['id'], table_df['name']))
        
        relationship_df_list = [] 
        relationship_df_all = pd.DataFrame(['No Relationships'])
        
        for table in app_tables:      
        
            r = requests.get(
                'https://api.quickbase.com/v1/tables/{}/relationships'.format(table[0])
                , proxies = self.proxies
                , headers = self.headers
            )
               
                     
            if r.json()['metadata']['numRelationships'] == 0:
                continue
            
            relationship_df = pd.DataFrame(r.json())
            
            relationship_df['tableId'] = table[0]
            relationship_df['tableName'] = table[1]
            relationship_df['appId'] = self.appid
            relationship_df['appName'] = self.app_info()['name'][0]
            
            relationship_df_list.append(relationship_df)       
            relationship_df_all = pd.concat(relationship_df_list)

        return relationship_df_all          
    
    def get_report(self, tableid, reportid, batch_size=500): 
        '''batch_size - optional arg for batch size of report load... 
        don't go over 1000 or records will fall out'''
        
        report_chunk_list = []
        skip = 0 
        records = 1
        
        while records != 0:
            
            params = {
              	'tableId': tableid  #bqtqseh2p
                , 'top': batch_size
                , 'skip': skip
            }
            
            r = requests.post(
            'https://api.quickbase.com/v1/reports/{}/run'.format(reportid), 
            params = params, 
            headers = self.headers,
            proxies = self.proxies
            )
            
            #get the data
            data = r.json()['data']
            
            
            records = len(data)
            
            if records != 0: 
                data_step_1 = [list(x.values()) for x in data]      
                data_step_2 = [[list(y.values())[0] for y in x] for x in data_step_1]  
                column_nums = list(data[0].keys())
                
                df = pd.DataFrame(data_step_2, columns = column_nums)
                
                #qb_df = union_df(qb_df, df)
                
                report_chunk_list.append(df)
                
                skip += batch_size
                print(str(skip - batch_size + len(data)) +  ' rows loaded')
        
        
        
        report_df = pd.concat(report_chunk_list)
        
        #rename columns 
        fields = r.json()['fields']
        
        column_names = {} #empty dictionary to add 
        for i in [[str(x['id']) ,  x['label'] ]for x in fields]:
            column_names[i[0]] = i[1]
        
        
        report_df = report_df.rename(columns=column_names)   
            
        return report_df
    
