from simple_salesforce import Salesforce
import pandas as pd 

#change to db location directory
db_location = r'C:\Users\c110846\Documents\salesforce_db'
os.chdir(db_location)

#connect to salesforce
sf = Salesforce('philip.lancaster@omnicare.com', 'password', '')  #leave 3rd arg blank


#query objects
object_name = 'account'
columns = 'Id, Name'

#create soql query for extraction... soql has major differences to sql... 
#read sf documentation on soql to better understand how it works
soql = 'SELECT {} FROM {} limit 10000'.format(columns, object_name)
    
#get results and convert to pandas df 
results = sf.query_all(soql)['records']
df = pd.DataFrame(results).drop(['attributes'], axis=1)       
    
#your sfdc query results now live in the df object... this can be loaded to excel, sql database, etc...

#################################
#Ways to find salesforce object names and column names/labels in sfdc
################################

#Get all object names in sf
object_names = [name['name'] for name in sf.describe()['sobjects']]


#change Account to any other object name from sfdc to get the column names and their labels
newdf = pd.DataFrame([['Account', x['name'], x['label']] for x in sf.Account.describe()['fields']], columns=['ObjectName','ColumnName','LabelName'])



'''
metadata_df = pd.DataFrame()

for i in object_names:

    exec("test = sf." + i.lower()+ ".describe()['fields']")

    print([[i, x['name'], x['label']] for x in test])
'''
