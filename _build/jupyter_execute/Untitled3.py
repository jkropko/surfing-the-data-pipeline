#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import math
from pandas_profiling import ProfileReport
import re
import collections

# Import warnings and add a filter to ignore them
import warnings
warnings.simplefilter('ignore')
# Import XGBoost
import xgboost
# XGBoost Classifier
from xgboost import XGBClassifier
# Classification report and confusion matrix
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
# Cross validation
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split

# To plot the graphs
import matplotlib.pyplot as plt
import seaborn as sn


# In[2]:


url = 'https://github.com/uvasds-sportsanalyticsclub/NBA_Shotlog/raw/main/Data/nba_shotlog_train.csv'
nba = pd.read_csv(url)
nba


# In[3]:


profile = ProfileReport(nba, 
                        title='Pandas Profiling Report',
                        html={'style':{'full_width':True}},
                       minimal=True)
profile.to_notebook_iframe()


# We convert minutes and seconds to separate columns:

# In[4]:


nba[['minute', 'second']] = nba['time'].str.split(':', 1, expand=True)
nba['time'] = nba['minute'].astype('int') + (nba['second'].astype('int')/60)


# In[5]:


nba['location_x_feet'] = nba['location_x'] * (94/nba['location_x'].max())
nba['location_x_feet'] = abs(nba['location_x_feet'] - 47)
nba['location_y_feet'] = nba['location_y'] * (50/nba['location_x'].max())
nba['location_y_feet'] = abs(nba['location_y_feet'] - 25)
nba['distance'] = ((nba['location_x_feet'])**2 + (nba['location_y_feet']-47)**2)**.5


# In[6]:


nba.query("time < 0.3").shot_type.unique()


# In[7]:


nba['distance'] = ((nba['location_x_feet'])**2 + (nba['location_y_feet']-47)**2)**.5


# In[8]:


nba.dtypes


# In[9]:


j = [[int(s) for s in re.findall(r'\b\d+\b', x)] for x in nba.shot_type]
d = [max(k, default=0) for k in j]
logic = [max(k, default=0) > 30 for k in j]
nba.loc[logic]


# In[10]:


nba['distance'].loc[logic] = np.array(d)[logic]


# In[11]:


tok = [s.split() for s in nba['shot_type']]
words = [x for xs in tok for x in xs]


# In[12]:


counter = collections.Counter(words)
topwords = [d[0] for d in counter.most_common()[1:23]]
topwords

for w in topwords:
    nba[w] = [w in s for s in nba['shot_type']]


# In[13]:


corr_matrix = nba[topwords].corr().abs()

# Select upper triangle of correlation matrix
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))

# Find features with correlation greater than 0.95
to_drop = [column for column in upper.columns if any(upper[column] > 0.95)]

# Drop features 
nba.drop(to_drop, axis=1, inplace=True)


# In[14]:


nba['date'] = pd.to_datetime(nba['date'])


# In[15]:


nba.dtypes


# In[16]:


nba.drop(['Unnamed: 0', 'home_team', 'away_team', 'location_x', 'location_y', 
             'location_x_feet', 'location_y_feet','shot_type', 'shoot_player', 
            'minute', 'second'], axis=1, inplace=True)


# In[17]:


y = nba['current_shot_outcome']
X = nba.drop(['current_shot_outcome'], axis=1)


# In[18]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)


# In[19]:


model = XGBClassifier(max_depth=2, n_estimators=30, enable_categorical=True)
model


# In[20]:


# Initialize the KFold parameters
kfold = KFold(n_splits=5)
# Perform K-Fold Cross Validation
results = cross_val_score(model, X_train, y_train, cv=kfold)
# Print the average results
print("Accuracy: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))


# In[21]:


model.fit(X_train, y_train)


# In[ ]:




