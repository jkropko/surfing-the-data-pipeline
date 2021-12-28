#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask
from flask_notifications import Notifications

# Corresponding information for brokers and Celery
config = {...}
celery = FlaskCeleryExt(app).celery
redis = StrictRedis(host=redis_host)


# In[ ]:




