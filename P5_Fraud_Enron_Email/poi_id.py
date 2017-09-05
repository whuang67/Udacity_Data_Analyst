#!/usr/bin/python

import sys
import pickle
import numpy as np
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data, test_classifier

### Task 1: Select what features you'll use.
features_list = ["poi", "total_payments", "other", "bonus", "expenses", "from_this_person_to_poi"]
                                                                        ### This one is for new feature

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
del data_dict["TOTAL"]

### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
my_dataset = data_dict
### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
### log (-restricted_stock_deferred + C) is the new feature that I tried.
# x = np.log(-data[:, 4] + max(data[:, 4]) + 1)
labels, features = targetFeatureSplit(data)
### Even though new feature is created, I choose not to use it.
features_ = [e[1:5] for e in data]

### Task 4: Try a varity of classifiers

#######################################################
### The task 4 and following one will code together ###
#######################################################

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script.


features_list = ["poi", "exercised_stock_options", "other", "restricted_stock", "expenses", "total_payments"]
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)
del data_dict["TOTAL"]
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features_ = targetFeatureSplit(data)


from sklearn.preprocessing import StandardScaler
features_ = StandardScaler().fit_transform(features_)

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import precision_score, recall_score
from sklearn.neighbors import KNeighborsClassifier
# Naive Bayes
from sklearn.naive_bayes import GaussianNB
clf_NB = GaussianNB().fit(features_, labels)
print "The training precision and recall of Naive Bayes are {:.4f} and {:.4f} respectively.\n".format(
    precision_score(labels, clf_NB.predict(features_)),
    recall_score(labels, clf_NB.predict(features_)))

# Decision Tree
from sklearn.tree import DecisionTreeClassifier
parameters = {"criterion": ["gini", "entropy"], "min_samples_split":[2, 4, 6, 8, 10, 12, 14]}
clf_DT = GridSearchCV(DecisionTreeClassifier(random_state = 42), parameters, cv = 10, scoring = "recall")
clf_DT.fit(features_, labels)
print "Best Parameters for Decision Tree:"
print clf_DT.best_params_
print "The training precision and recall of Decision Tree are {:.4f} and {:.4f} respectively.\n".format(
    precision_score(labels, clf_DT.predict(features_)),
    recall_score(labels, clf_DT.predict(features_)))

# K Nearest Neighbors
parameters = {"n_neighbors": [3, 5, 7, 9, 11, 13, 15, 17, 19, 21]}
clf_KNN = GridSearchCV(KNeighborsClassifier(), parameters, cv = 10, scoring = "recall")
clf_KNN.fit(features_, labels)
print "Best Parameters for K Nearest Neighbors:"
print clf_KNN.best_params_
print "The training precision and recall of KNN are {:.4f} and {:.4f} respectively.\n".format(
    precision_score(labels, clf_KNN.predict(features_)),
    recall_score(labels, clf_KNN.predict(features_)))

clf = clf_DT.best_estimator_

### print out the test metrics
# print test_classifier(clf, my_dataset, features_list)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)


# print test_classifier(clf_NB,  my_dataset, features_list)
print test_classifier(clf, my_dataset, features_list)
# print test_classifier(clf_KNN, my_dataset, features_list)