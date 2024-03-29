# -*- coding: utf-8 -*-
"""nb kaggle

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LuO753RwxYcGSDzUkOt-obw3KVuL4UoQ
"""

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import tensorflow as tf
import os
from sklearn.naive_bayes import GaussianNB
from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

#load the csv file

train_dataset_url = "https://raw.githubusercontent.com/szieying/kaggle/master/naivekaggle.csv"

train_dataset_fp = tf.keras.utils.get_file(fname=os.path.basename(train_dataset_url),
                                           origin=train_dataset_url)

print("Local copy of the dataset file: {}".format(train_dataset_fp))

df=pd.read_csv('/root/.keras/datasets/naivekaggle.csv')

#Initialize Gaussian Naive Bayes
clf = GaussianNB()

# Split-out validation dataset
array = df.values
X = array[:,1:11]
Y = array[:,11]

print(Y)

"""1. 准备stroke dataset
2. 放到github
3. 改到可以print 出 x and y


----------------------------------------------------------------------------------------------------------------------

1. 试看150的可以work 吗

p_APLT,HPLD,IHD,AGE0,P_ACEI,SMOKER,P_ARB,P_LL



------------------------------------------------------------------------------------------------------------------------

1.
"""

# One-third of data as a part of test set
validation_size = 0.33

seed = 7
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)

# Test options and evaluation metric
scoring = 'accuracy'

#Fitting the training set
clf.fit(X_train, Y_train) 

#Predicting for the Test Set
pred_clf = clf.predict(X_validation)

#Prediction Probability
prob_pos_clf = clf.predict_proba(X_validation)[:, 1]

#Create the prediction file by concatenation of the original data and predictions
#Reshaping needed to perform the concatenation
pred_clf_df = pd.DataFrame(pred_clf.reshape(660,1))
#Column renaming to indicate the predictions
pred_clf_df.rename(columns={0:'Prediction'}, inplace=True)

#reshaping the test dataset
X_validation_df = pd.DataFrame(X_validation.reshape(660,10))
Y_validation_df = pd.DataFrame(Y_validation.reshape(660,1))

#concatenating the two pandas dataframes over the columns to create a prediction dataset
pred_outcome = pd.concat([X_validation_df, pred_clf_df], axis=1, join_axes=[X_validation_df.index])

pred_outcome.rename(columns = {0:'gender', 1:'age', 2:'hypertension', 3:'heart_disease', 4:'ever_married', 5:'work_type', 6:'Residence_type', 7:'avg_glucose_level', 8:'bmi', 9:'smoking_status'}, inplace=True)

del df['Id']

#merging the prediction with original dataset
pred_comp = pd.merge(df,pred_outcome, on=['gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 'work_type', 'Residence_type', 'avg_glucose_level', 'bmi', 'smoking_status'])

#print top 10 lines of the final predictions
print((pred_comp).head(10))
print ("\n")

#Save the file to csv
pred_comp.to_csv('NBPredictions.csv', sep=',')

#Save the file to Excel
from pandas import ExcelWriter

writer = ExcelWriter('NBPredictions.xlsx')
pred_outcome.to_excel(writer,'Sheet1')
Y_validation_df.to_excel(writer,'Sheet2')
writer.save()


#Model Performance
#setting performance parameters
kfold = model_selection.KFold(n_splits=10, random_state=seed)

#calling the cross validation function
cv_results = model_selection.cross_val_score(GaussianNB(), X_train, Y_train, cv=kfold, scoring=scoring)

#displaying the mean and standard deviation of the prediction
msg = "%s: %f (%f)" % ('NB accuracy', cv_results.mean(), cv_results.std())
print(msg)

print(X_validation_df)

print(pred_comp)

print(len(Y_validation_df))

print(pred_outcome)