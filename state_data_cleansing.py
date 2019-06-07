import pandas as pd
import numpy as np


url = 'https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States'


"""
df_states = pd.read_html(url, header=1)
df_states = df_states[0]
df_states.set_index('Capital', inplace=True)
pd.DataFrame.to_csv(df_states, 'states.csv')
"""

df_states = pd.read_csv('states.csv', index_col = 0)

#rename index and columns
df_states.index.rename(['State'], inplace=True)
df_states.rename(columns={ df_states.columns[0] : 'state_abbr', \
    df_states.columns[1] : 'capital_city', df_states.columns[2] : 'largest_city', \
    df_states.columns[3] : 'date_est', df_states.columns[4] : 'population', \
    df_states.columns[5] : 'total_area_mi', df_states.columns[6] : 'total_area_km', \
    df_states.columns[7] : 'land_area_mi', df_states.columns[8] : 'land_area_km', \
    df_states.columns[9] : 'water_area_mi', df_states.columns[10] : 'water_area_km', \
    df_states.columns[11] : 'representatives'}, inplace=True)

#clean data (some rows values populated 1 column to the left
#for the states whose capital was also their largest city)

for i, row in df_states.head(3).iterrows():
    print(str(row.name) + ' ' + str(row[11]))

    if np.isnan(row[11]):
        df_states.loc[str(row), 'representatives'] = 'Test' #trying to get this to change the value...no luck....


print(df_states.head().iloc[:, 9:12])

 
"""
    print(i[11])
    if np.isnan(i[11]):
        i[11] = 'Test'
        #df_states.at['', '']
    print(str(i[11]) + ' - ' + str(i))
print(df_states.iloc[0:3,9:12])
"""
