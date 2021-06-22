#!/usr/bin/env python
# coding: utf-8

# In[2]:


from sklearn.datasets import load_files
from sklearn.pipeline import Pipeline
from sklearn import metrics
import numpy as np
import pickle
import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB,GaussianNB
from sklearn.svm import SVC
from nltk.tokenize import RegexpTokenizer
from nltk import PorterStemmer
from nltk.corpus import stopwords
from gensim.models import FastText
import gensim
import re
from scipy.stats import reciprocal, uniform
from sklearn.model_selection import RandomizedSearchCV



categories = ['Business', 'Entertainment', 'Living', 'Metro', 'Shopping', 'Sports', 'Tech']

train_data = load_files(container_path='C:\\DMA_project3\\CC\\text\\train', categories=categories, shuffle=True,
                        encoding='utf-8', decode_error='replace')
test_data = load_files(container_path='C:\\DMA_project3\\CC\\text\\test', categories=categories, shuffle=True,
                        encoding='utf-8', decode_error='replace')
class Tokenizer:
    def __init__(self):
        self.tkn = RegexpTokenizer(r'\w+')        
        self.stemmer = PorterStemmer()
        self.stopWords = set(stopwords.words('english'))
    def __call__(self, doc):
        text = re.sub('\d+', '', doc)
        tokens = self.tkn.tokenize(text)
        tokens = [word.lower() for word in tokens]
        tokens = [token for token in tokens if token not in self.stopWords]
        tokens = [word for word in tokens if len(word) >= 2]
        tokens = [self.stemmer.stem(word) for word in tokens]
        return tokens
    
# TODO - 2-1-1. Build pipeline for Naive Bayes Classifier
clf_nb = Pipeline([
    ('vect', CountVectorizer(tokenizer=Tokenizer())),
    ('tfidf', TfidfTransformer()),
    ('clf', MultinomialNB(alpha=0.016))
])
clf_nb.fit(train_data.data, train_data.target)

# TODO - 2-1-2. Build pipeline for SVM Classifier
clf_svm = Pipeline([
    ('vect', CountVectorizer(tokenizer=Tokenizer())),
    ('tfidf', TfidfTransformer()),
    ('clf', SVC(kernel='linear', coef0=1, C=1))
])
clf_svm.fit(train_data.data, train_data.target)

docs_test = test_data.data

predicted = clf_nb.predict(docs_test)
# predicted = clf_svm.predict(docs_test)

print("NB accuracy : %d / %d" % (np.sum(predicted==test_data.target), len(test_data.target)))
# print(metrics.classification_report(test_data.target, predicted, target_names=test_data.target_names))
# print(metrics.confusion_matrix(test_data.target, predicted))

TEAM = 1

with open('DMA_project3_team%02d_nb.pkl' % TEAM, 'wb') as f1:
    pickle.dump(clf_nb, f1)

with open('DMA_project3_team%02d_svm.pkl' % TEAM, 'wb') as f2:
    pickle.dump(clf_svm, f2)

