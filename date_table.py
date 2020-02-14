import pandas as pd 
from datetime import datetime, timedelta
import math
from dateutil.relativedelta import relativedelta

startdate = datetime(2010,1,1)
enddate = datetime(2021,1,1)
dates = []

while startdate < enddate:
    dates.append(startdate)
    startdate += timedelta(days=1)

date_table = pd.DataFrame(dates, columns=['DateTimeObject'])

#float, int, bool, datetime64[ns], timedelta[ns], and object. 
#In addition these dtypes have item sizes, e.g. int64 and int32.
#also a 'category' object.


list_of_date_formats = [
['%x', 'Date', 'datetime64[ns]'], ['%x %X', 'DateTime', 'datetime64[ns]'], 
['%a', 'DayShort', 'category'], ['%A', 'DayLong', 'category'], ['%w', 'Day', 'int16'],
['%d', 'DayOfMonth', 'int16'], ['%b', 'MonthShort', 'category'], 
['%B', 'MonthLong', 'category'], ['%m', 'Month', 'int16'], ['%y', 'YearShort', 'int16'], 
['%Y', 'Year', 'int16'], ['%j', 'DayOfYear', 'int16'], ['%U', 'WeekOfYear', 'int16'], 
['%W', 'WeekOfYearMonday', 'int16'], ['%Y%m','YYYYMM','category']
]

for i in list_of_date_formats:
    date_table[i[1]] = date_table['DateTimeObject'].apply(lambda x: x.strftime(i[0])).astype(i[2])


#Start/End of Week and Month
date_table['StartOfWeek'] = date_table.apply(lambda x: (x['DateTimeObject']
    - timedelta(int(x['Day']))).strftime('%x'), axis=1).astype('datetime64[ns]')

date_table['EndOfWeek'] = date_table.apply(lambda x: (x['StartOfWeek'] + 
          timedelta(days=6)).strftime('%x'), axis=1).astype('datetime64[ns]')

date_table['StartOfMonth'] = date_table.apply(lambda x: (x['DateTimeObject'] 
    - timedelta(days = int(x['DayOfMonth']) -1)).strftime('%x')
    , axis=1).astype('datetime64[ns]')

date_table['EndOfMonth'] = date_table.apply(lambda x: (x['StartOfMonth'] 
    + relativedelta(months = 1, days = -1)).strftime('%x'), axis=1).astype('datetime64[ns]')



#Quarter columns
date_table['YYYYQQ'] = date_table['YYYYMM'].apply(lambda x: str(x[0:4]) + 'Q' + str(math.ceil(int(x[-2:])/3))).astype('category')
date_table['QQ'] = date_table['YYYYQQ'].apply(lambda x: x[-2:]).astype('category')
date_table['Quarter'] = date_table['YYYYQQ'].apply(lambda x: int(x[-1:])).astype('int16')

#Check memory size of table 
#pd.concat([date_table.dtypes, date_table.memory_usage()], axis=1, sort=False).rename(columns={0: "dtype", 1: "memory"})
