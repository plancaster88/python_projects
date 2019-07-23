# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 11:27:04 2019

@author: a278881
"""

import os 
import pandas as pd
from datetime import datetime as dt 
import seaborn as sns

'''
#r in front is a raw string... 
path = r''
#change to the directory 
os.chdir(path)
'''

df = pd.read_csv('sonar.all-data')


df.head()


df.groupby('R').count().iloc[:,1]


sns.heatmap(df.isnull(),yticklabels=False,cbar=False)

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.svm import SVC

X = df.drop('R', axis=1)
y = df['R']

X_train, X_test, y_train, y_test = \
    train_test_split(X, y, test_size=0.3,random_state=101)
    

print('\nSVM')   
svm_model = SVC() 
svm_model.fit(X_train,y_train)
predictions = svm_model.predict(X_test)
matrix = confusion_matrix(y_test, predictions)
#print(classification_report(y_test,rf_predict))
print('Accuracy Tot: ' + str(accuracy_score(y_test, predictions)))
print('Accuracy - 0: ' + str((matrix.diagonal()/matrix.sum(axis=1))[0]))
print('Accuracy - 1: ' + str((matrix.diagonal()/matrix.sum(axis=1))[1]))    
    

param_grid = {'C': [0.1,1, 10, 100, 1000],
              'gamma': [1,0.1,0.01,0.001,0.0001], 'kernel': ['rbf']} 


from sklearn.model_selection import GridSearchCV

grid = GridSearchCV(SVC(),param_grid,refit=True,verbose=3)
grid.fit(X_train,y_train)
#grid.best_params_
grid.best_estimator_

grid_predictions = grid.predict(X_test)
matrix = confusion_matrix(y_test, grid_predictions)
print(classification_report(y_test,rf_predict))


cm = confusion_matrix(y_test, grid_predictions).astype(float)
class_list = list(y_test.drop_duplicates().sort_values())


#confusion matrix heatmap unlabeled
#sns.heatmap(data=cm, annot=True, cmap='Blues').set_title('Confusion Matrix')


#confusion matrix heatmap w/ labels & %s

#convert to float so math works out in the loop
cm = cm.astype(float)

#to get CM to %s 
#for i in range(len(cm)):
#    cm[i] = cm[i]/sum(cm[i])*100


#confusion matrix heatmap labeled
sns.heatmap(data=pd.DataFrame(cm, columns=(class_list)
            , index=(class_list))
            , annot=True, cmap='Blues', fmt='g'
            ).set_title('Confusion Matrix by %')


    
    
    

