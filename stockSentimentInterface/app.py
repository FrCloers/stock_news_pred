from datetime import date
import pandas
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

def choice_parameter():
    st.title("Choose a date")
    session = requests.Session()
    rows = pd.DataFrame(run_query("""SELECT * from ticker;"""))
    with st.form("my_form"):
        col1, col2 = st.columns(2)
        date = st.date_input("date", key="date")
        ticker = st.selectbox("ticker", rows)
        value = (date, ticker)
        submitted =  st.form_submit_button("Submit")

        if submitted:
            st.write("Result")
            news = pd.DataFrame(run_query("""SELECT title, content FROM news WHERE `date` = %s AND ticker = %s""", value), 
                                columns=['title', 'content'])
            st.text(news)


if __name__ == '__main__':
    conn = init_connection()

    st.title("Predict stocks prices with sentimental analysis")


    choice_parameter()
