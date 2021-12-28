#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import requests
import json


# In[2]:


url = 'https://data.virginia.gov/resource/bre9-aqqr.json'
r = requests.get(url, headers = {'User-agent': 'J. Kropko, class example for UVA data science: jkropko@virginia.edu'})
r


# In[3]:


data = pd.json_normalize(json.loads(r.text))
data


# In[4]:


data.query("locality == 'Albemarle'")


# In[ ]:




