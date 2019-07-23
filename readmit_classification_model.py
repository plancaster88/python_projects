import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import os 


#r in front is a raw string... 
path = r'\\midp-sfs-006\aetnabttrhlthlastfls\Philip Lancaster\Python\ReadmitModel'
#change to the directory 
os.chdir(path)

#use the following sql to get the original dataset then pickle 
'''
import pyodbc
import pickle 

connStr = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server}; \
                            SERVER=SRVQNXTRPTLAPROD; \
                            DATABASE=la_temp; \
                            Trusted_Connection=yes')


sql = " select * from la_ops_temp.dbo.vAdmit_Classifier\
        where dischargedate between\
        '2017-01-01' and dateadd(m, -2, getdate())"

df = pd.read_sql(sql,connStr)

#pickle 
df.to_pickle("./authadmits.pkl")
'''
#unpickle 
df = pd.read_pickle("./authadmits.pkl")

#make date it's on df until we need to make train/test dfs 
df_date = df['AdmitDate']
df.drop('AdmitDate', axis=1, inplace=True)

#include feature backward elimination step? | include scaling step?
scale_step = False
feature_elimination_step = False


#look at data head and type
#df.head()
#df.info()


#See if any NULL values exist
#plt.figure(figsize = (10,10))
#sns.heatmap(df.isnull(),yticklabels=False,cbar=False)

#only a few nulls in diag category... replace with blank
df.fillna('UNKNOWN_DIAG', inplace=True)

#drop unneeded columns
df.drop('Aetna_GrpDesc', inplace=True, axis=1) #too many diag groups
df.drop('GeoRegion', inplace=True, axis=1) #Have a region field already
#df.drop('DischargeMonth', axis=1, inplace=True)
df.drop('Admit_Key', inplace=True, axis=1) 

#clean up Ethnicity 
df['Ethnicity'] = df['Ethnicity'].apply(lambda x: x.upper().strip())

#get dummy variables for categorical features
#pd.get_dummies(df['DischargeMonth'],drop_first=True)

#method to do all categorical features at once
for i in list(zip(list(df.columns), list(df.dtypes))):
    if i[1] == 'object':
        yadumdum = pd.get_dummies(df[i[0]]) #,drop_first=True)
        df = pd.concat([df,yadumdum],axis=1)
        df.drop(i[0], inplace = True, axis=1)      

import statsmodels.formula.api as sm
import numpy as np

# drop features w/ p value > .05
if feature_elimination_step == True:
    X_constant = pd.DataFrame(np.ones((len(df), 1)).astype(int)
        , columns=['Constant'])
    en = df['Readmit_Numerator']
    
    booly = True
    
    while booly:
        
        ex = pd.concat([X_constant, df.drop('Readmit_Numerator', axis=1)], axis=1)
        reg_OLS = sm.OLS(endog=en, exog=ex).fit()
        #reg_OLS.summary() #shows coef, R-sq, P, etc... 
        if reg_OLS.pvalues.sort_values(ascending=False).index[0] != 'Constant':
            pval = reg_OLS.pvalues.sort_values(ascending=False)[0]
            feature = reg_OLS.pvalues.sort_values(ascending=False).index[0] 
        else:
            pval = reg_OLS.pvalues.sort_values(ascending=False)[1]
            feature = reg_OLS.pvalues.sort_values(ascending=False).index[1] 
        
        
        if pval > .05 and feature != 'Constant':
            df.drop(feature, axis = 1, inplace=True)  
            print(pval, feature)
        else:
            booly = False
    

#scale data
from sklearn.preprocessing import StandardScaler
         
if scale_step == True:

    scaler = StandardScaler()
    scaler.fit(df.drop('Readmit_Numerator',axis=1))
    StandardScaler(copy=True, with_mean=True, with_std=True)
    scaled_features = scaler.transform(df.drop('Readmit_Numerator',axis=1))
    
    df_scaled = pd.DataFrame(scaled_features,columns=df.drop(
            'Readmit_Numerator',axis=1).columns)
 
    df = pd.concat([df_scaled, df['Readmit_Numerator']], axis=1) #pull date back in 


#create test and train dataframes
df = pd.concat([df, df_date], axis=1)

df_test = pd.DataFrame(df[df['AdmitDate'].apply(lambda x: str(x)[0:4]) == '2019'])
df = pd.DataFrame(df[df['AdmitDate'].apply(lambda x: str(x)[0:4]) != '2019'])

#date was only used to seperate test and train
df.drop('AdmitDate', inplace=True, axis=1) 
df_test.drop('AdmitDate', inplace=True, axis=1) 
      
df = df.reset_index().drop('index', axis=1)


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression 
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB,GaussianNB
from sklearn.svm import SVC

#pickle to test Neural Network on Azure Notebooks
# got to 0 - 67% Recall and 1 - 67% Recall
'''
import pickle 
pkl_df = pd.DataFrame(
        pd.concat([df['Readmit_Numerator']
            , df.drop('Readmit_Numerator', axis=1)]
            , axis=1)
        )      
#rename columns     
pkl_df.columns = [str(i) for i in list(range(len(df.columns)))] 
  

pkl_df_test = pd.DataFrame(
        pd.concat([df_test['Readmit_Numerator']
            , df_test.drop('Readmit_Numerator', axis=1)]
            , axis=1)
        )      
#rename columns     
pkl_df_test.columns = [str(i) for i in list(range(len(df.columns)))] 
  
pkl_df.to_pickle("./classified_project.pkl")
pkl_df_test.to_pickle("./classified_project_test.pkl")
'''



# Separate majority and minority classes
df_majority = df[df['Readmit_Numerator']==0]
df_minority = df[df['Readmit_Numerator']==1]


###############################################################################
#UPSAMPLE
#https://elitedatascience.com/imbalanced-classes
###############################################################################

from sklearn.utils import resample

# Upsample minority class
df_minority_upsampled = resample(df_minority, 
                                 replace=True,     # sample with replacement
                                 n_samples=len(df_majority),   # to match majority class
                                 random_state=101) # reproducible results
 
# Combine majority class with upsampled minority class
df_upsampled = pd.concat([df_majority, df_minority_upsampled])




X_train, X_test, y_train, y_test = \
    train_test_split(df_upsampled.drop('Readmit_Numerator', axis=1)
        , df_upsampled['Readmit_Numerator'], test_size=0.0, random_state=101)


X_test = df_test.drop('Readmit_Numerator', axis=1).reset_index().drop('index', axis=1)
y_test = df_test['Readmit_Numerator'].reset_index().drop('index', axis=1)
    

#create class to handle creating and assessing multiple models... 
class ClassificationModel:
    def __init__(self, model, X_train, X_test, y_train, y_test, title= 'No Model title'): 
         
        self.title = title    
        
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        
        self.model = model.fit(self.X_train,self.y_train)
        
        self.y_pred = model.predict(self.X_test)
        self.y_pred_proba = model.predict_proba(self.X_test) #gives the % that the model assigned 
        
        
        self.detail = pd.concat([self.y_test.reset_index()
            , pd.DataFrame(self.y_pred)
            , pd.DataFrame(self.y_pred_proba, columns=['risk_left','risk']
                ).drop('risk_left',axis=1)
            , self.X_test.reset_index().drop('index', axis=1)
                ], axis=1).set_index('index')
        
    
    def classification_report(self):
        print('\n',self.title,'- Classification Report')
        print(classification_report(self.y_test, self.y_pred))

    def confusion_matrix(self):
        print('\n',self.title,'- Confusion Matrix')
        print(confusion_matrix(self.y_test, self.y_pred))
        
    
models_to_run = {
      'LOGISTIC REGRESSION' : LogisticRegression()
    , 'RANDOM FOREST' : RandomForestClassifier(max_depth=5,n_estimators=100)
    , 'DECISION TREE' : DecisionTreeClassifier(max_depth=5)
    , 'GRADIENT BOOST' : GradientBoostingClassifier(n_estimators=5, learning_rate=1.0, max_depth=3)
    #, 'KNN' : KNeighborsClassifier(n_neighbors=3)
    }
    

#run classification report on all models
for model_title, model in models_to_run.items():
    print(ClassificationModel(model,X_train,X_test
        ,y_train,y_test,model_title).classification_report())   



#free play with models using the ClassificationModel class
'''
gb_model = GradientBoostingClassifier(n_estimators=5, learning_rate=1.0
                                      , max_depth=3)



gb_model_class = ClassificationModel(gb_model,X_train,X_test,y_train,y_test
                               ,title='Gradient Boost')
'''

#Original Method before class was created 
'''
print('\nLOGISIC REGRESSION US')
logmodel = LogisticRegression()
logmodel.fit(X_train,y_train)    
predictions = logmodel.predict(X_test)
risk_pct = logmodel.predict_proba(X_test) #gives the % that the model assigned 
matrix = confusion_matrix(y_test, predictions)
print(classification_report(y_test,predictions))
'''

#Grid search method to determine best parameters for models
'''
from sklearn.model_selection import GridSearchCV
clf = LogisticRegression()
grid_values = {'penalty': ['l1', 'l2'],'C':[0.001,.009,0.01,.09,1,5,10,25]}
grid_clf_acc = GridSearchCV(clf, param_grid = grid_values)
grid_clf_acc.fit(X_train, y_train)
'''

#ROC Curve
'''
from sklearn.metrics import roc_curve, auc
fpr, tpr, threshold = roc_curve(y_test, my_model.y_pred)
roc_auc = auc(fpr, tpr)

import matplotlib.pyplot as plt
plt.title('Receiver Operating Characteristic')
plt.figure(figsize=[8,8])
plt.plot(fpr, tpr, 'b--', label = 'AUC RF = %0.2f' % roc_auc)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1], c='black')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()
'''

#elbow method
'''
error_rate = []

# Will take some time
for i in range(1,5):
    print(i)
    
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train,y_train)
    pred_i = knn.predict(X_test)
    error_rate.append(np.mean(pred_i != y_test))

    
plt.figure(figsize=(10,6))
plt.plot(range(1,4),error_rate,color='blue', linestyle='dashed', marker='o',
         markerfacecolor='red', markersize=10)
plt.title('Error Rate vs. K Value')
plt.xlabel('K')
plt.ylabel('Error Rate')    
''' 
    
#Classifier Summary Table
'''
df_0 = df[df['Readmit_Numerator']==0].describe().transpose()
df_0['Readmitted'] = '0'

cols = list(df_0)  
cols.insert(0, cols.pop(cols.index('Readmitted')))
df_0 = df_0.reindex(columns= cols)   


df_1 = df[df['Readmit_Numerator']==1].describe().transpose()
df_1['Readmitted'] = '1'


cols = list(df_1)  
cols.insert(0, cols.pop(cols.index('Readmitted')))
df_1 = df_1.reindex(columns= cols)   


pd.concat([df_1, df_0]).reset_index(
        ).rename(columns={'index':'Feature'}).sort_values(
                by=['Feature','Readmitted']).set_index(['Feature', 'Readmitted'])
'''

#coefficients
'''
coeff_df = pd.DataFrame(list(zip(X_train.columns.tolist()\
        , logmodel.coef_.tolist()[0]))\
        , columns=['Feature','Coefficient'])

print(coeff_df.sort_values('Coefficient'))

coeff_df = pd.DataFrame(list(zip(X_train.columns.tolist()\
        , logmodel.coef_.tolist()[0]))\
        , columns=['Feature','Coefficient'])

print(coeff_df)
'''
