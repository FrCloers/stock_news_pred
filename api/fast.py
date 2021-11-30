from fastapi  import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from stockLstmModel.data import get_stocksprice_data
from newsSentimentModel.data import connect_to_db, get_news_data
from tweetSentimentModel.data import get_tweet_data
from stockSentimentModel.data import get_stocksentiment_data


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
    return {'Hello from cloud run CD'}


@app.get("/get_stocksprice_data")
def stocks_data():
    connnection = connect_to_db()
    df = get_stocksprice_data(connnection.cursor())
    return df.head(5)

@app.get("/get_news_data")
def news_data():
    connnection = connect_to_db()
    df = get_news_data(connnection.cursor())
    return df.head(5)

@app.get("/get_tweet_data")
def tweets_data():
    connnection = connect_to_db()
    df = get_tweet_data(connnection.cursor())
    return df.head(5)