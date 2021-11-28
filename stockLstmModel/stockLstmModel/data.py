import pandas as pd
import numpy as np
import pymysql
import os
from stockLstmModel.utils import simple_time_tracker
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
def get_stocksprice_data():
    """Function to get the data from\
       the stocksapi table in the database"""
    #connection with the db
    connection = connect_to_db()
    cursor = connection.cursor()

    # Create a new query that selects the entire contents of 'ticker'
    sql = "SELECT ticker, `date`, stock_price FROM stocksprice"
    cursor.execute(sql)
    return pd.DataFrame(cursor.fetchall(), columns=['ticker', 'date', 'stock_price'])

@simple_time_tracker
def upload_LSTM_prediction(df):
    """Function to upload the LSTM prediction\
        in the database\
        in predictionmodel table\
        in the stock_api_pred column"""
    #connect to the dB
    connection = connect_to_db()
    cursor = connection.cursor()

    #transform the DataFrame in a list of list
    stock_list = list(df[['stock_api_pred','date', 'ticker']].values)
    stock_list = np.array(stock_list)
    stock_list = stock_list.tolist()

    for LSTM_prediction, date, ticker in stock_list:
        try:
            #If the prediction does not yet exist, it is inserted into the database,
            #otherwise it is updated
            sql = """INSERT INTO prediction (stock_api_pred, `date`, ticker) \
                    VALUES (%s, %s, %s)"""
            #Values you want to insert
            values = (LSTM_prediction, date, ticker)
            cursor.execute(sql, values)
            connection.commit()

        except pymysql.Error as err:
            if err.args[0] == 1062:
                print('Duplicate entry, updating the values')
                #SQL query
                sql = """UPDATE prediction SET stock_api_pred=%s WHERE `date`=%s AND ticker=%s"""
                #Values you want to insert
                values = (LSTM_prediction, date, ticker)
                cursor.execute(sql, values)
                connection.commit()

if __name__ == "__main__":
    print('test')
    print(get_stocksprice_data().head())
