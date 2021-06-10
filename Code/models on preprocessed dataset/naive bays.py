# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 19:04:26 2021

@author: somar
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler
from imblearn.over_sampling import SMOTE 
data=pd.read_csv("train.csv")
data.info()
for i in data.columns:
    if data[i].dtype=="object":
        print(data[i].value_counts())
cat=[]
num=[]
for i in data.columns:
    if data[i].dtype=="object":
           cat.append(i)
            
    else:
            num.append(i)
#convert categorial to numeric            
data =pd.get_dummies(data, columns=cat,drop_first=True)  
# Scale only columns that have values greater than 1
to_scale = [col for col in data.columns if data[col].max() > 1]
mms = MinMaxScaler()
scaled = mms.fit_transform(data[to_scale])
scaled = pd.DataFrame(scaled, columns=to_scale)

# Replace original columns with scaled ones
for col in scaled:
    data[col] = scaled[col]
   
X = data.drop('Response', axis=1)
X = X.drop('id', axis=1)

y = data['Response']  
sm = SMOTE(random_state=42)

X_sm, y_sm = sm.fit_resample(X, y)
X_train, X_test, y_train, y_test = train_test_split(X_sm, y_sm, test_size=0.25 , random_state=1)
NB_model = GaussianNB()
NB_model.fit(X_train, y_train)
y_train_predict = NB_model.predict(X_train)
model_score = NB_model.score(X_train, y_train)
print(model_score)
print(metrics.confusion_matrix(y_train, y_train_predict))
print(metrics.classification_report(y_train, y_train_predict))
y_test_predict = NB_model.predict(X_test)
model_scoreNB = NB_model.score(X_test, y_test)
print(model_scoreNB)
print(metrics.confusion_matrix(y_test, y_test_predict))
print(metrics.classification_report(y_test, y_test_predict))