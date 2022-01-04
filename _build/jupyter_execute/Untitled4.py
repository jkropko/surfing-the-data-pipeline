#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
url = "https://raw.githubusercontent.com/jkropko/DS-6001/master/localdata/anes_example_toplines.csv"
anes = pd.DataFrame({'x':[1,2,3]})


# In[2]:


anes.columns


# In[ ]:





# In[3]:


help(anes)


# In[4]:


anes.corr()


# In[5]:


get_ipython().run_line_magic('pinfo2', 'pd.read_csv')


# In[ ]:




