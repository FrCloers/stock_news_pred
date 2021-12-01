from fastapi  import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from stockLstmModel.data import get_stocksprice_data
from newsSentimentModel.data import connect_to_db, get_news_data
from tweetSentimentModel.data import get_tweet_data
import os
import connect_db
import pandas as pd
from dotenv import load_dotenv

#load environment variable
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get('/')
def index():
     return {
            os.environ.get('DB_HOST'), 
            os.environ.get('DB_USER'),
            os.environ.get('DB_PASS'),
            os.environ.get('DB_NAME')
     }

@app.get("/get_stocksprice_data")
def stocks_data():
    pool = connect_db.container_connect_bd()
    connection = pool.connect()
    sql = "SELECT ticker, `date`, stock_price FROM stocksprice WHERE ticker = %s"
    values = ('AMZN', )
    df=pd.DataFrame(connection.execute(sql, values).fetchall(), columns=['ticker', 'date', 'stock_price'])
    return df.head(5)

@app.get("/get_news_data")
def news_data():
    try:
        connnection = connect_to_db()
        df = get_news_data(connnection.cursor())
        return df.head(5)
    except:
        pass

@app.get("/get_tweet_data")
def tweets_data():
    connnection = connect_to_db()
    df = get_tweet_data(connnection.cursor())
    return df.head(5)