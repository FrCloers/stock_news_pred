#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# For sending GET requests from the API
import requests
# For saving access tokens and for file management when creating and adding to the dataset
import os
# For dealing with json responses we receive from the API
import json
# For displaying the data after
import pandas as pd
# For saving the response data in CSV format
import csv
# For parsing the dates received from twitter in readable formats
import datetime
import dateutil.parser
import unicodedata
#To add wait time between requests
import time


# In[ ]:


os.environ['TOKEN'] = '******************************************************************************************************'


# In[ ]:


def auth():
    return os.getenv('TOKEN')


# In[ ]:


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


# In[ ]:


def create_url(keyword, start_date, end_date, max_results = 100):
    
    search_url = "https://api.twitter.com/2/tweets/search/all" #Change to the endpoint you want to collect data from

    #change params based on the endpoint you are using
    query_params = {'query':keyword ,
                    'start_time': start_date,
                    'end_time': end_date,
                    'max_results': max_results,
                    #'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                    'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                    #'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                    #'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                    'next_token': {}}
    return (search_url, query_params)


# In[ ]:


def connect_to_endpoint(url, headers, params, next_token=None ):
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


# In[ ]:





# In[ ]:


#Inputs for the request
bearer_token = auth()
headers = create_headers(bearer_token)
keyword = "$TSLA \AND stock"
start_time = "2020-11-26T00:00:00.000Z"
end_time = "2021-11-26T00:00:00.000Z"
max_results = 100


# In[ ]:


url = create_url(keyword, start_time,end_time, max_results)
json_response = connect_to_endpoint(url[0], headers, url[1])


# In[ ]:


#json_response


# In[ ]:


import time

results_list = []

url,  query_params = create_url(keyword, start_time,end_time, max_results)
json_response = connect_to_endpoint(url, headers, query_params)
data = json_response["data"]
results_list.append(data)

while True:
    next_token = json_response['meta'].get('next_token', None)
    
    
    if next_token is None:
        break
        
    else:
        print(next_token)
        #query_params["next_token"] = next_token
        print(query_params)
        time.sleep(2)
        json_response = connect_to_endpoint(url, headers, query_params, next_token=next_token)
        
        data = json_response["data"]
        results_list.append(data)


# In[ ]:


len(results_list)


# In[ ]:


created_at=[]
text=[]

for page in results_list:
  for tweet in page:
      created_at.append(tweet['created_at'])
      text.append(tweet['text'])


# In[ ]:


df1 = pd.DataFrame(created_at, columns=['created_at'])
df2 = pd.DataFrame(text, columns=['text'])

df3= pd.concat([df1, df2], axis=1)
df3


# In[ ]:


df3.to_csv('Tesla.csv')


# In[ ]:





# 
