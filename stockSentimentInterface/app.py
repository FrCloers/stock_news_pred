import datetime as dt
import streamlit as st
import requests
import pandas as pd
import numpy as np
import connect_db
import os

from dateutil.relativedelta import relativedelta

# Perform query.
# Uses st.cache to only rerun when the query changes or after 10 min.
#creation dt connection
pool = connect_db.init_db_connection()
connection = pool.connect()

#Perform API
session = requests.Session()
def fetch(session, url):
    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}

#setup page
st.set_page_config(layout="wide")

#title page
st.title("Predict stock prices with sentiment analysis")

#Select parameters query
rows = pd.DataFrame(connection.execute("""SELECT * from ticker;""").fetchall())
ticker = st.selectbox("Ticker", rows)
date = st.date_input('Date', key='Date')
value = (date, ticker)

st.subheader(f"Theses are the news and the tweets about the {ticker} on {date}")
col1, col2, col3 = st.columns(3)
with col1:
    st.header('News')
    news = pd.DataFrame(connection.execute("""SELECT title, content FROM news WHERE `date` = %s AND ticker = %s""", value).fetchall(), 
                        columns=['title', 'content'])
    st.dataframe(news)

    

with col2:
    st.header('Tweets')
    news = pd.DataFrame(connection.execute("""SELECT tweet FROM tweets WHERE `date` = %s AND ticker = %s""", value).fetchall(), 
                        columns=['tweet'])
    st.dataframe(news)

with col3:
    st.header('Stock prices')
    ## Range selector
    
    st.table(pd.DataFrame([[date - relativedelta(years=2), date, date + dt.timedelta(days=10)]],
                    columns=['start',
                            'selected',
                            'end'],
                    index=['date']))

    value =(ticker, date - relativedelta(years=2), date + dt.timedelta(days=10) )
    sql="""SELECT date, stock_price \
        FROM stocksprice \
        WHERE ticker = %s AND (`date` BETWEEN %s AND %s)"""

    stock = pd.DataFrame(connection.execute(sql, value).fetchall(), 
                        columns=['date', 'stock_price'])
    stock = stock.set_index('date')
    st.line_chart(stock)

st.header(f"Prediction 3 Features {ticker}")
st.subheader("News sentiment analysis, Tweets sentiment analysis and LSTM")
sql="""SELECT p.`date`, stock_price, next_day_pred \
       FROM prediction p INNER JOIN stocksprice s \
       ON s.`date` = p.`date` AND s.ticker = p.ticker \
       WHERE p.ticker = %s AND (p.`date` BETWEEN %s AND %s)"""

stock = pd.DataFrame(connection.execute(sql, value).fetchall(), 
                        columns=['date', 'stock_price', 'prediction'])

stock.sort_values(by='date', ascending=False, inplace=True)
stock = stock.set_index('date')
stock['shift_prediction'] = stock['prediction'].shift(-1)
stock['error'] = stock['shift_prediction'] - stock['stock_price'] 
st.line_chart(stock)
st.write(stock)
            