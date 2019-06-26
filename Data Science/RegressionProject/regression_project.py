
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import os

df = pd.read_csv('Ecommerce Customers')

#inspect dataframe
df.head()
df.info()

#pull data into power bi and visualize data
url = 'https://app.powerbi.com/view?r=eyJrIjoiYmQ0MjNlO\
GEtNmZlZi00ZGJiLTk3MzMtNDg2MTc1ZDViOWMyIiwidCI6IjNlN2M1N\
TE0LTY0NGItNGUwMy1iM2RhLTJmZjg1ZmM5NWNmMiIsImMiOjN9'
webbrowser.open_new(url)

#Add Email Domain as a feature
df['EmailDomain'] = df['Email'].apply(lambda x: x.split('@')[-1])

#look at top domains
df[['EmailDomain','Email']].groupby('EmailDomain'
     ,sort=True).count().sort_values(by=['Email'], ascending=False).head()

#these are the only top email services:
popular_domains = ['hotmail.com','gmail.com','yahoo.com']

#create popular email domain feature
df['EmailDomainSpecific'] =  df['EmailDomain'].apply(
      lambda x: x in popular_domains)*1

#see if anything is correlated
plt.figure(figsize=(8,8))
sns.heatmap(df.corr(), cmap='coolwarm')

#import libraries
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import statsmodels.formula.api as sm

#create dataframes for model dependent variable (y) and independent variables (x)
X = df[['Avg. Session Length','Time on App','Time on Website',\
        'Length of Membership','GeneralEmail']]
y = df['Yearly Amount Spent']




#OLS Regression Results

#make constant
X_constant = pd.DataFrame(np.ones((len(X), 1)).astype(int), columns=['Constant'])

regressor_OLS = sm.OLS(endog=y, exog=pd.concat([X_constant, X], axis=1)).fit()
print(regressor_OLS.summary())

#backward elimination 

X.drop('GeneralEmail', inplace=True, axis=1)
print(sm.OLS(endog=y, exog=pd.concat([X_constant, X], axis=1)).fit().summary())

X.drop('Time on Website', inplace=True, axis=1)
print(sm.OLS(endog=y, exog=pd.concat([X_constant, X], axis=1)).fit().summary())


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=101) 
#random_state allows the outcome to always be the same... good for testing not production

#create model
lm = LinearRegression()
lm.fit(X_train,y_train)

#find intercept
print(lm.intercept_)

#coefficients
coeff_df = pd.DataFrame(lm.coef_,X.columns,columns=['Coefficient'])
print(coeff_df)

#predictions
predictions = lm.predict(X_test)

#scatterplot of predictions
plt.scatter(y_test,predictions)

#residuals
sns.distplot((y_test-predictions),bins=50)

#Actuals vs Predictions
print('\nActuals\nTotal: ', round(sum(y_test),2)
   , 'Avg: ' ,round(np.average(y_test),2)
   , 'Min: ' ,round(np.min(y_test),2)
   , 'Max: ' ,round(np.max(y_test),2))
print('\nPredictions\nTotal: ', round(sum(predictions),2)
   , 'Avg: ' , round(np.average(predictions),2)
   , 'Min: ' ,round(np.min(predictions),2)
   , 'Max: ' ,round(np.max(predictions),2))


