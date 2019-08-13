# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 16:21:38 2019

@author: Aghapy
"""

# Import Used Libraries.
import csv
import random
import pandas as pd
import numpy as np
from openpyxl.utils import dataframe
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import seaborn as sns
import matplotlib.pyplot as plt
import math
from matplotlib import colors as cs
from scipy.misc import imshow
from scipy.stats import pearsonr
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import scale
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest
from sklearn import tree
# import graphviz
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import f1_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer, precision_score, recall_score, confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

magic = pd.read_csv("magic.data", sep=',')  # Reads a magic csv file.
magic.classHG = pd.get_dummies(magic['classHG'], drop_first=True)  # class H=1  G=0

# balancing the data

x = magic.drop("classHG", axis=1)
y = magic["classHG"]

# Visualization
plt.title('line plot')  # line plot
plt.plot(x, y)
plt.show()

magic.hist()  # histogram

plt.matshow(magic.corr())  # correlation matrix
plt.title('correlation matrix')
plt.show()

magic.boxplot(grid=False)
plt.show()

# dataset resampling
classHG_count = magic.classHG.value_counts()
count_class_G, count_class_H = magic.classHG.value_counts()
# Divide by class
G_class = magic[magic['classHG'] == 0]
H_class = magic[magic['classHG'] == 1]
G_class_under = G_class.sample(count_class_H)
magic_under = pd.concat([G_class_under, H_class], axis=0)
x_under = magic_under.drop("classHG", axis=1)
y_under = magic_under["classHG"]
magic_under.hist()
plt.show()

# split data into training and testing
x_train, x_test, y_train, y_test = train_test_split(x_under, y_under, test_size=0.3, random_state=1)


# feature selection
# hshoofha delw2ty


def print_stats(estimator):
    y_pred_train = estimator.predict(x_train)
    y_pred_test = estimator.predict(x_test)
    print('Train Set Accuracy : ', accuracy_score(y_train, y_pred_train))
    print('Train Set Precision : ', precision_score(y_train, y_pred_train))
    print('Train Set Recall : ', recall_score(y_train, y_pred_train))
    print('Train F-Score for each class : ', f1_score(y_train, y_pred_train, average=None))
    print('Train Mean F-Score for both classes : ', f1_score(y_train, y_pred_train, average='macro'))
    print('Train Confusion Matrix : ', confusion_matrix(y_train, y_pred_train))
    print('----------------------------------------------------------------------')
    print('Test Set Accuracy : ', accuracy_score(y_test, y_pred_test))
    print('Test Set Precision : ', precision_score(y_test, y_pred_test))
    print('Test Set Recall : ', recall_score(y_test, y_pred_test))
    print('Test F-Score for each class : ', f1_score(y_test, y_pred_test, average=None))
    print('Test Mean F-Score for both classes : ', f1_score(y_test, y_pred_test, average='macro'))
    print('Test Confusion Matrix : ', confusion_matrix(y_test, y_pred_test))
    print('----------------------------------------------------------------------')


# KNN
num_jobs = 9


def kNearestNeighborsFunction(start_n, end_n):
    parameters = {'n_neighbors': list(range(start_n, end_n))}
    KNNC = KNeighborsClassifier(n_jobs=num_jobs)
    gKnn = GridSearchCV(KNNC, parameters, scoring='f1_macro', cv=5, n_jobs=num_jobs)
    gKnn.fit(x_train, y_train)
    print('Best N found at ', gKnn.best_params_)
    print('Best Mean F-Score ', gKnn.best_score_)
    ns = gKnn.cv_results_['param_n_neighbors']
    ns_score = gKnn.cv_results_['mean_test_score']
    plt.title('Mean F-Score with different neighbors')
    plt.plot(ns, ns_score)
    plt.xlabel('# of neighbours')
    plt.ylabel('Validation Mean F-Score')
    plt.show()
    print_stats(gKnn)


# logistic regression
def LR():
    logmodel = LogisticRegression()
    logmodel.fit(x_train, y_train)
    print_stats(logmodel)
