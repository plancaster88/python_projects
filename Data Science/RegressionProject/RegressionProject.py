
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import os


path = r'C:\Users\phili\Desktop\Python Bootcamp\Course Files\11-Linear-Regression'
os.chdir(path)


df = pd.read_csv('Ecommerce Customers')

#inspect dataframe
df.head()
df.info()

#pull data into power bi and visualize data


#Add Email Domain as a feature
df['EmailDomain'] = df['Email'].apply(lambda x: x.split('@')[-1])


df[['EmailDomain','Email']].groupby('EmailDomain'
     ,sort=True).count().sort_values(by=['Email'], ascending=False).head()

popular_domains = ['hotmail.com','gmail.com','yahoo.com']

df['EmailDomainSpecific'] =   df['EmailDomain'].apply(
      lambda x: x in popular_domains, 1, 0)


df_email = pd.get_dummies(df['EmailDomainSpecific'], drop_first=True)

df = pd.concat([df, df_email], axis=1)

#rename dummy column
df.rename(columns={True:'GeneralEmail'}, inplace=True)


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


#make constant
X_constant = pd.DataFrame(np.ones((len(X), 1)).astype(int), columns=['Constant'])

#OLS Regression Results
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
coeff_df

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


