import os 
import pandas as pd 
from io import StringIO 
import win32com.client

file = r'C:\Users\c110846\Desktop\New folder\ EXTERNAL  Report  Bed Report Email run at 1 1 2020 12 18 AM.msg'

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

msg = outlook.OpenSharedItem(file)

sender = msg.SenderName
sender_email = msg.SenderEmailAddress
sent = msg.SentOn
subject = msg.Subject
body = msg.Body

#count_attachments = msg.Attachments.Count
#if count_attachments > 0:
#    for item in range(count_attachments):
#        print msg.Attachments.Item(item + 1).Filename


del outlook, msg

column = 'MicrostrategyFacility ID'

for row_num in range(1, body.count('\n')):
    try:
        
        test = pd.read_csv(StringIO(body), skiprows=row_num, nrows=1, sep ='\t')
        
        if test.columns[0] == column:
            #print(num)
            break
            
    except:
        print('error')
   
print(row_num, test.columns[0])
 
z = pd.read_csv(StringIO(body), skiprows=row_num, skipfooter=5, sep ='\t')
