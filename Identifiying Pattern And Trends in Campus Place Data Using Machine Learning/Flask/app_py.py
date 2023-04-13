# -*- coding: utf-8 -*-
"""app.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Kb4yZVwKhgaaXRCDZY0QcilTO2cHETY1

# *IDENTIFYING PATTERNS AND TRENDS IN CAMPUS PLACEMENT DATA USING MECHINE LEARNING*

**Importing The Libraries**
"""

import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.model_selection import cross_val_score
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler 
import joblib
from sklearn.metrics import accuracy_score

"""**Read The Dataset**"""

df = pd.read_csv("/content/collegePlace.csv") 
df.head()

df.shape

sns.pairplot(df)

corr = df.corr()

ax = sns.heatmap(corr, vmin = -1, vmax = 1, annot = True)
  bottom, top = ax.get_ylim()
  ax.set_ylim(bottom + 0.5, top - 0.5)
  plt.show()
  corr

plt.figure(figsize=(12,5))
plt.subplot(121)
sns.distplot(df['CGPA'],color='r')

plt.figure(figsize=(12,5))
plt.subplot(121)
sns.distplot(df['CGPA'],color='r')

plt.figure(figsize = (10,6), dpi = 100)
color_palette = sns.color_palette("BuGn_r")
sns.set_palette(color_palette)
sns.countplot(x = "PlacedOrNot", data = df)

df.info()

df.isnull().sum()

"""Handling Outlire"""

df.describe()

df['Gender'].value_counts()

df['Stream'].value_counts()

df=df.replace(['Male'], [0])
df =df.replace(['Female'], [1])

df=df.replace(['Computer Science', 'Information Technology', 'Electronics And Communication', 'Mechanical', 'Electrical', 'Civil'],
                [0,1,2,3,4,5])

df=df.drop(['Hostel'], axis=1)

df

df.info()

def transformationplot(feature):
  plt.figure(figsize=(12,5))
  plt.subplot(1,2,1)
  sns.distplot(feature)

transformationplot(np.log(df['Age']))

df = df.drop(['Stream'], axis=1)

df

X = df.drop(columns = 'PlacedOrNot', axis=1)
Y = df['PlacedOrNot']

import joblib
joblib.dump(X,"placement")

print(X)

print(Y)

scaler = StandardScaler()

scaler.fit(X)

standardized_data = scaler.transform(X)

print(standardized_data)

X = standardized_data
Y = df['PlacedOrNot']

X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.2, stratify=Y, random_state=2)

print(X.shape, X_train.shape, X_test.shape)

classifier = svm.SVC(kernel='linear')

classifier.fit(X_train, Y_train)

X_test_prediction = classifier.predict(X_test)
y_pred= accuracy_score(X_test_prediction, Y_test)
y_pred

X_test

X_train_prediction = classifier.predict(X_train)
training_data_accuracy = accuracy_score(X_train_prediction, Y_train)

print('Accuracy score of training data : ', training_data_accuracy)

from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.model_selection import cross_val_score

best_k = {"Regular":0}
best_score = {"Regular":0}
for k in range(3,50,2):
  knn_temp = KNeighborsClassifier(n_neighbors=k)
  knn_temp.fit(X_train, Y_train)
  knn_temp_pred = knn_temp.predict(X_test)
  score = metrics.accuracy_score(Y_test, knn_temp_pred) * 100
  if score >= best_score["Regular"] and score < 100:
    best_score["Regular"] = score
    best_k["Regular"] = k

print("---Results---\nK: {}\nScore: {}".format(best_k, best_score))
knn =  KNeighborsClassifier(n_neighbors=best_k["Regular"])
knn.fit(X_train, Y_train)
knn_pred = knn.predict(X_test)
testd = accuracy_score(knn_pred, Y_test)

knn_pred

print('Accuracy score of the test data using KNN : ', testd)

knn_pred_1 = knn.predict(X_train)
traind = accuracy_score(knn_pred_1, Y_train)
traind

knn_pred_1

X_train.shape

Y_train.shape

import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from tensorflow.keras import layers

classifier = Sequential()
classifier.add(keras.layers.Dense(6,activation = 'relu', input_dim = 6))
classifier.add(keras.layers.Dropout(0.50))
classifier.add(keras.layers.Dense(6,activation = 'relu'))
classifier.add(keras.layers.Dropout(0.50))
classifier.add(keras.layers.Dense(6,activation = 'sigmoid'))

loss_1 = tf. keras.losses.BinaryCrossentropy()
classifier.compile(optimizer = 'Adam', loss = loss_1 , metrics = ['Accracy'])

#classifier.fit(X_train, Y_train, batch_size = 20, epochs = 100)

#pred = classifire.predict(X-test)
#pred = (pred > 0.5)
#pred

#from sklearn.metrics import confusion_matrix
#cm = confusion_matrix(Y_test, pred)
#cm

import pickle
pickle.dump(knn,open("placement.pkl",'wb'))
model = pickle.load(open('placement.pkl', 'rb'))

input_data = [22,0,2,1,8,1,3,4,7]
prediction = knn.predict(input_data)
print(prediction)

if(prediction[0] == 0):
  print('not placed')
else:
  print('placed')