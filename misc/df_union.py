def union_df(maindf, tempdf):
    if  maindf.empty:
        maindf = tempdf
    else:
        maindf = pd.concat([maindf, tempdf]) #union all in sql...basically
    return maindf
