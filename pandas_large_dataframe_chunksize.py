
import pandas as pd 


def union_df(maindf, tempdf):
    if  maindf.empty:
        maindf = tempdf
    else:
        maindf = pd.concat([maindf, tempdf]) #union all in sql...basically
    return maindf


nppes_df = pd.DataFrame()
    
nrows_num = 100000
nrows_total = 0
columns = ['NPI','Certification Date', 'NPI Deactivation Date', 'NPI Reactivation Date']

for df_chunk in pd.read_csv(r'C:\Users\a278881\Desktop\npidata_pfile_20050523-20200809.csv'
                     , chunksize = nrows_num
                     , usecols = columns):

    
    new_df = df_chunk[df_chunk['Certification Date'].notnull()] 
    
    nppes_df = union_df(nppes_df, new_df)
    
    
    records = len(df_chunk)
     
    print(nrows_total + len(df_chunk))
    
    nrows_total += nrows_num
