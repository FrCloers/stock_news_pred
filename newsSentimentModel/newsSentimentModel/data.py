import pandas as pd
import pymysql
from utils import simple_time_tracker

def connect_to_db():
    """Function to make the connection with\
    the database and return the cursor"""
    connection = pymysql.connect(
        host='34.159.115.175',
        user='root',
        password='batch-735-berlin',
        db='db-stock-news-pred'
    )
    return connection.cursor()

@simple_time_tracker
def get_news_data():
    """Function to get the data from\
       the newsapi table in the database"""
    
    cursor = connect_to_db()
    # Create a new query that selects the entire contents of 'ticker'
    sql = "SELECT * FROM `ticker`"
    cursor.execute(sql)

    # Fetch all the records and use a for loop to print them one line at a time
    result = cursor.fetchall()
    for i in result:
        print(i)

def upload_news_sentiment():
    """Function to upload the sentiment news prediction \
        in the database\
        in predictionmodel table\
        in the tweet_api_sentiment column""" 
    pass

if __name__ == "__main__":
    print('test')
    get_news_data()