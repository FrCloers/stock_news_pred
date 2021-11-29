from datetime import date
import cufflinks as cf
import streamlit as st
import requests
import mysql.connector
import pandas as pd

# Initialize connection.
# Uses st.cache to only run once.
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

# Perform query.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
def run_query(query, values=None):
    with conn.cursor() as cur:
        cur.execute(query, values)
        return cur.fetchall()


#Perform API
session = requests.Session()
def fetch(session, url):
    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}

st.set_page_config(layout="wide")
st.title("Predict stocks prices with sentimental analysis")
conn = init_connection()

#sidebar
st.sidebar.subheader('query parameters')
date = st.sidebar.date_input('Date', key="date")
rows = pd.DataFrame(run_query("""SELECT * from ticker;"""))
ticker = st.sidebar.selectbox("Ticker", rows)
value = (date, ticker)

st.text(f"This is the newspaper and the tweets about the {ticker} on {date}")

col1, col2 = st.columns(2)
with col1:
    st.header('News')
    news = pd.DataFrame(run_query("""SELECT title, content FROM news WHERE `date` = %s AND ticker = %s""", value), 
                    columns=['title', 'content'])
    st.dataframe(news)

with col2:
    st.header('Tweets')
    news = pd.DataFrame(run_query("""SELECT tweet FROM tweets WHERE `date` = %s AND ticker = %s""", value), 
                    columns=['tweet'])
    st.dataframe(news)
#parameter_form()
