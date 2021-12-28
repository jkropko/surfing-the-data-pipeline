#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import numpy as np
import pandas as pd
import hashlib
url = 'https://ncimpcapstone.club/?challengeCode=1234'


# In[2]:


r = requests.get(url)


# In[3]:


r


# In[4]:


r.text


# In[5]:


json.loads(r.text)


# In[28]:


challengeCode = 1234
endpoint = 'https://ncimpcapstone.club'
verificationToken = 'elizabeth-karolina-felipe-nick-kropko'
m = hashlib.sha256(str(str(challengeCode)+verificationToken+endpoint).encode('utf-8'))
myDict = {'challengeResponse':m.hexdigest()}
myDict


# In[38]:


challengeCode = 1234
endpoint = 'https://ncimpcapstone.club'
verificationToken = 'elizabeth-karolina-felipe-nick-kropko'
challengeCode = str(challengeCode).encode('utf-8')
verificationToken = str(verificationToken).encode('utf-8')
endpoint = str(endpoint).encode('utf-8')
m = hashlib.sha256(challengeCode+verificationToken+endpoint)
myDict = {'challengeResponse':m.hexdigest()}
myDict


# In[39]:


challengeCode+verificationToken+endpoint


# In[25]:


challengeCode.encode('utf-8').decode('utf-8')


# In[36]:


hashlib.sha256(b'hello').hexdigest()


# In[43]:


bytes(1234)


# In[ ]:




