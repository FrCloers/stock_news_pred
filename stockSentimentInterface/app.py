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

@st.cache(ttl=600)
def run_query(query, values=None):
    return connection.execute(query, values)
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
st.title("Predict stocks prices with sentimental analysis")

#Select parameters query
rows = pd.DataFrame(run_query("""SELECT * from ticker;""").fetchall())
ticker = st.selectbox("Ticker", rows)
date = st.date_input('Date', key='Date')
value = (date, ticker)

st.subheader(f"This is the newspaper and the tweets about the {ticker} on {date}")
col1, col2, col3 = st.columns(3)
with col1:
    st.header('News')
    news = pd.DataFrame(run_query("""SELECT title, content FROM news WHERE `date` = %s AND ticker = %s""", value).fetchall(), 
                        columns=['title', 'content'])
    st.dataframe(news)

with col2:
    st.header('Tweets')
    news = pd.DataFrame(run_query("""SELECT tweet FROM tweets WHERE `date` = %s AND ticker = %s""", value).fetchall(), 
                        columns=['tweet'])
    st.dataframe(news)

with col3:
    st.header('stock prices')
    ## Range selector
    
    st.table(pd.DataFrame([[date - relativedelta(years=1), date, date + dt.timedelta(days=10)]],
                    columns=['start',
                            'selected',
                            'end'],
                    index=['date']))

    value =(ticker, date - relativedelta(years=1), date + dt.timedelta(days=10) )
    sql="""SELECT date, stock_price \
        FROM stocksprice \
        WHERE ticker = %s AND (`date` BETWEEN %s AND %s)"""

    stock = pd.DataFrame(run_query(sql, value).fetchall(), 
                        columns=['date', 'stock_price'])
    stock = stock.set_index('date')
    st.line_chart(stock)
    #plot stock price
    st.write(stock)
