import numpy as np 
import pandas as pd
from datetime import datetime
import time

while True:
    url_dict = {
    'GTX1050ti'     : 'http://www.nowinstock.net/computers/videocards/nvidia/gtx1050ti/'
    ,'GTX1060'      : 'http://www.nowinstock.net/computers/videocards/nvidia/gtx1060/'
    ,'GTX1070'      : 'http://www.nowinstock.net/computers/videocards/nvidia/gtx1070/'
    ,'GTX1070ti'    : 'http://www.nowinstock.net/computers/videocards/nvidia/gtx1070ti/'
    ,'GTX1080'      : 'http://www.nowinstock.net/computers/videocards/nvidia/gtx1080/'
    ,'GTX1080ti'    : 'http://www.nowinstock.net/computers/videocards/nvidia/gtx1080ti/'
    ,'GTX2060'    : 'http://www.nowinstock.net/computers/videocards/nvidia/rtx2060/'
    ,'GTX2070'    : 'http://www.nowinstock.net/computers/videocards/nvidia/rtx2070/'
    ,'GTX2080'    : 'http://www.nowinstock.net/computers/videocards/nvidia/rtx2080/'
    ,'GTX2080ti'    : 'http://www.nowinstock.net/computers/videocards/nvidia/rtx2080ti/'


    }

    def union_df(df, tempdf):
        if  df.empty:
            df = tempdf
        else:
            df = pd.concat([df, tempdf]) #union all in sql...basically
        return df

    df = pd.DataFrame()

    for gpu, url in url_dict.items():
        tempdf = pd.read_html(url, header=0)
        tempdf = tempdf[0]
        tempdf['GPU'] = gpu
        df = union_df(df, tempdf)

    df = df[df.Name != 'Ebay : All Models'] #filter out ebay rows
    df = df[df['Status1'] == 'In Stock'] #select  where in stock
    df['Last Price1'] = df['Last Price1'].str.replace('$', '')
    df['Last Price1'] = df['Last Price1'].str.replace(',', '').astype(float)

    #df = df[df['Last Price1'] <= 1000.00] #select  where in stock
    df['Name'] = df['Name'].str.lower() #convert to lower for the conditional check below 

    #hard code gtx1060 gpus as 6g or 3g
    df['GPUdd'] = pd.np.where(df.Name.str.contains("6g|1060 fe|p10600a-10l"), df['GPU'] + ' 6g',
                    pd.np.where(df.Name.str.contains("3g|p10610a-10l"), df['GPU'] + ' 3g',
                    df['GPU']))

    
    df['Name'] = df['Name'].str.upper() #covnert back to upper
    df.sort_values(['GPUdd', 'Last Price1'], ascending=[True, True], inplace=True) #sort by GPUs and 

    df['Last Price1'] = '$' + df['Last Price1'].astype(str)

    #Add a blank row after each GPU

    gpu_list = df['GPUdd'].unique()
    blankline_df = pd.DataFrame()

    for gpu in gpu_list:
        tempdf = df[df['GPUdd'] == gpu]

        blankline_df = union_df(blankline_df, tempdf)

        blank = pd.Series([],index=[]) #adds a blank row to the end of dataframe
        blankline_df = blankline_df.append(blank, ignore_index=True)   
        
    blankline_df.fillna('-', inplace=True)
    blankline_df.rename(index=str, columns={'GPUdd': 'GPU Type', 'Name' : 'Model','Last Price1': 'Last Price','Last Stock1': 'Last Stock'}, inplace=True)


    #Next section converts the table to an html table
    html_output = pd.DataFrame.to_html(blankline_df[['GPU Type', 'Model', 'Last Price', 'Last Stock']], index=False, classes="table table-sm", border="0")
    html_output = html_output.replace('<tr style="text-align: right;">', '<tr>' )

    html_start = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <title>GPUs</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css">
    </head>
    <body>
    <div class="container">
    <h2>Current costs for in stock GPUs</h2>
    """

    html_end = '</div></body></html>'

    updated_time = '<i>Updated: ' + datetime.now().strftime('%Y-%m-%d') + ' at ' + datetime.now().strftime('%H:%M') + '</i><br>'

    html_all = html_start + updated_time +  html_output + html_end

    Html_file = open("GPUs.html","w")
    Html_file.write(html_all)
    Html_file.close()

    x = np.random.randint(600, 900)
    time.sleep(x)
