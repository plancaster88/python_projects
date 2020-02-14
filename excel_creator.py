

import pandas as pd
import os
import re #regular expressions
from datetime import datetime

file_location = r'c:\Users\c110846\Desktop\Local Files\Python'


# Change directory to file location
os.chdir(file_location)

# Current working directory
os.getcwd()

# List all files in the directory
os.listdir()

# Regex pull of all files in a folder 
file_keyword = 'tes'
file_extension = 'xlsx'

files = [f for f in os.listdir() if re.findall('^{}.*[.]{}$'\
         .format(file_keyword.lower(), file_extension.lower()),f.lower())] 
    
#regex guide https://www.w3schools.com/python/python_regex.asp
# ^ is starts with
# {} is a placeholder for .format()
# . is any 1 character
# * is any # of occurences (including 0) of previous character (.* = % in SQL)
# $ is ends with
# [] is virtually the same as SQL regex
    


# Create a function to get hexidecimal code for formatting 
def rgb_to_hex (r,g,b):
    '''
    function to give hexidecimal color code for RGB numbers
    '''
    rgb = '#'
    for i in [r,g,b]:
        rgb += hex(i)[2:]
    
    return rgb

rgb_to_hex()


####################################################################
# CREATE AN EXCEL SPREADSHEET AND FORMAT 
####################################################################

# Read excel file
df = pd.read_excel('test.xlsx')

# Create new column
df['d'] = df['b'] + df['c']

#sort values
df = df.sort_values('d', ascending=False)

#make header for excel spreadsheet
df_header = pd.DataFrame(['Philip Lancaster',datetime.strftime(datetime.now()
                , '%m-%d-%Y')])

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='MyOutput', index=False, startrow=3)

# Add a header to the spreadsheet
df_header.to_excel(writer, sheet_name='MyOutput', index=False, header=False)

# Make worbook object 
workbook = writer.book

# Create worksheet object
MyOutput_worksheet = writer.sheets['MyOutput']

# https://xlsxwriter.readthedocs.io/working_with_conditional_formats.html
MyOutput_worksheet.conditional_format('D5:D' + str(4+len(df)) 
    , {'type': 'data_bar', 'bar_solid': True,})# 'bar_color':'#daeef3'})

# Close the Pandas Excel writer and output the Excel file.
writer.save()
