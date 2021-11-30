#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd
import numpy as np

import matplotlib.pyplot as plt


# In[14]:


df= pd.read_csv('Tesla sentiment_final.csv', lineterminator='\n')


# In[15]:


df


# In[16]:


df = df.drop(columns  =['Unnamed: 0.1', 'Unnamed: 0', 'text'])


# In[17]:


df


# In[18]:


df1=df.rename(columns={'created_at' : 'date'})


# In[19]:


df2= df1.rename(columns={'cleaned_tweets' : 'title'})


# In[20]:


df2


# In[21]:


df2.to_csv('Tesla(for 7 months) Database ')


# # Construct new columns for aggregated sentiment result per day - preprocessing for model

# In[ ]:





# In[22]:


#create a function to get out the boolean result per row 
def preprocess_sentiment(X):
    return X.split()[0][1:]


# In[23]:


df2["sentiment_result"] = df2["sentiment"].apply(preprocess_sentiment)
df2["sentiment_result"]


# In[24]:


df2["date"] = pd.to_datetime(df2["date"]).dt.date


# In[25]:


#create a new column positive
df2["positive"] = df2["sentiment_result"].apply(lambda X: 1 if X =="POSITIVE" else  0)


# In[26]:


#create a new column negative
df2["negative"] = df2["sentiment_result"].apply(lambda X: 1 if X =="NEGATIVE" else  0)


# In[27]:


df2


# In[28]:


df2['ticker'] = 'TSLA'


# In[29]:


df2


# # create the final sentiment label

# In[30]:


#group by per date and ticker
df2_sentiment_count = df2.groupby(by=["date", "ticker"]).agg(sum)


# In[ ]:





# In[31]:


#reset index to have date per row
df2_sentiment_count.reset_index(drop=False, inplace=True)


# In[32]:


#create a new column to 
df2_sentiment_count["majority"] = df2_sentiment_count["positive"]- df2_sentiment_count["negative"]


# In[33]:


df2_sentiment_count["class_label"] = df2_sentiment_count["majority"].apply(lambda x: 1 if x>0 else 0)
df2_sentiment_count.drop(columns=["positive", "negative", "majority"], inplace=True)
df2_sentiment_count


# In[34]:


df2_sentiment_count.to_csv(" Tesla twitter_stocks_sentiment.csv")


# In[ ]:




