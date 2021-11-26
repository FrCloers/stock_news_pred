import pandas as pd
import pymysql
import os
from utils import simple_time_tracker
from dotenv import load_dotenv


#load environment variable
load_dotenv()

def connect_to_db():
    """Function to make the connection with\
    the database and return the cursor"""
    connection = pymysql.connect(
        host=os.environ.get('DB_HOST'), 
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        db=os.environ.get('DB_NAME')
    )
    return connection.cursor()

@simple_time_tracker
def get_news_data():
    """Function to get the data from\
       the newsapi table in the database"""
    
    #connection with the db
    cursor = connect_to_db()

    # Create a new query that selects the entire contents of 'ticker'
    sql = "SELECT id, ticker, `date`, title, content FROM news"
    cursor.execute(sql)
    return pd.DataFrame(cursor.fetchall(), columns=['id', 'ticker', 'date', 'title', 'content'])

def upload_news_sentiment():
    """Function to upload the sentiment news prediction \
        in the database\
        in predictionmodel table\
        in the tweet_api_sentiment column""" 
    cursor = connect_to_db()
    sql = "SELECT id, ticker, `date`, title, content FROM news"
    if cursor.execute(sql):
        return "update done"
    else:
        return "error update"

if __name__ == "__main__":
    print('test')
    df = get_news_data()
    print(df.head(5))
