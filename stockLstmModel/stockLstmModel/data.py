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

def get_stocksprice_data():
    """Function to get the data from\
       the stocksapi table in the database"""
    #connection with the db
    cursor = connect_to_db()

    # Create a new query that selects the entire contents of 'ticker'

    sql = "SELECT ticker, `date`, stock_price FROM stocksprice"
    cursor.execute(sql)
    return pd.DataFrame(cursor.fetchall(), columns=['ticker', 'date', 'stock_price'])

def upload_LSTM_prediction():
    """Function to upload the LSTM prediction\
        in the database\
        in predictionmodel table\
        in the stock_api_pred column"""
    pass

if __name__ == "__main__":
    print('test')
    print(get_stocksprice_data().head())
