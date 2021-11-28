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
    return connection

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

@simple_time_tracker
def upload_news_sentiment(date, ticker, sentiment):
    """Function to upload the sentiment news prediction \
        in the database\
        in predictionmodel table\
        in the tweet_api_sentiment column""" 
    #connect to the dB
    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        #If the prediction does not yet exist, it is inserted into the database,
        #otherwise it is updated
        sql = """INSERT INTO prediction (news_api_sentiment, `date`, ticker) \
                 VALUES (%s, %s, %s)"""
        #Values you want to insert
        values = (sentiment, date, ticker)
        cursor.execute(sql, values)
        connection.commit()

    except pymysql.Error as err:
        if err.args[0] == 1062:
            print('Duplicate entry, updating the values')
            #SQL query
            sql = """UPDATE prediction SET news_api_sentiment=%s WHERE `date`=%s AND ticker=%s"""
            #Values you want to insert
            values = (sentiment, date, ticker)
            cursor.execute(sql, values)
            connection.commit()

if __name__ == "__main__":
    print('test')
    #df = get_news_data()
    #print(df.head(5))

    #test upload_news_sentiment 
    print(upload_news_sentiment("2012-01-01", "GOOGL", "good sentiment22"))
