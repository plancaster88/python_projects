
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

#USE KNN TO CLASSIFY UNKNOWN DATA

#1  Get the Data
df = pd.read_csv("Classified Data",index_col=0)

#2  Explore data 
df.head()
df.describe().transpose()
#sns.pairplot(data=df, hue='TARGET CLASS')

#see if classes are balanced 
df.groupby('TARGET CLASS').count().iloc[:,0]

#3  Standardize the Variables w/ a scaler
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaler.fit(df.drop('TARGET CLASS',axis=1))
scaled_features = scaler.transform(df.drop('TARGET CLASS',axis=1))
df_feat = pd.DataFrame(scaled_features,columns=df.columns[:-1])

#4  Train Test Split
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

X = df_feat
y = df['TARGET CLASS']

#create train and test 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)

#5  Create KNN 
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train,y_train)
y_pred = knn.predict(X_test)

from sklearn.metrics import confusion_matrix, classification_report

#show results 
print(classification_report(y_test,y_pred))
cm = confusion_matrix(y_test, y_pred)

print('Accuracy  - ' , round((cm[1,1] + cm[0,0])/(sum(cm[0]) + sum(cm[1])), 3))
print('Class 0 A - ' , round(cm[0,0]/sum(cm[0]), 3))
print('Class 1 A - ' ,round(cm[1,1]/sum(cm[1]), 3))


#94.3% accuracy w/ 5 neighbors... 
#lets see if the model can be improved by using the elbow method 

#7  Choosing a K Value.... Elbow Method 
error_rate = []

for i in range(1,40):
    
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train,y_train)
    pred_i = knn.predict(X_test)
    error_rate.append(np.mean(pred_i != y_test))

#use the graph to determine a good k value 
plt.figure(figsize=(10,6))
plt.plot(range(1,40),error_rate,color='blue', linestyle='dashed', marker='o',
         markerfacecolor='red', markersize=10)
plt.title('Error Rate vs. K Value')
plt.xlabel('K')
plt.ylabel('Error Rate')

#k=18 looks like a good value based on the graph from the elbow method 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)
knn = KNeighborsClassifier(n_neighbors=18)
knn.fit(X_train,y_train)

y_pred = knn.predict(X_test)


print(classification_report(y_test,y_pred))

cm = confusion_matrix(y_test, y_pred)

print('A - ' , round((cm[1,1] + cm[0,0])/(sum(cm[0]) + sum(cm[1])), 3))
print('0 - ' , round(cm[0,0]/sum(cm[0]), 3))
print('1 - ' ,round(cm[1,1]/sum(cm[1]), 3))

#accuracy improved to 95.3% 
