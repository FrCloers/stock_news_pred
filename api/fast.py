import sys
from fastapi  import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from stockLstmModel.data import get_stocksprice_data
from newsSentimentModel.newsSentimentModel.data import connect_to_db, get_news_data

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
    return {'stock predcti with sentiment analysis'}

@app.get("/get_stocksprice_data")
def index():
    df = get_stocksprice_data()
    return df.head(5)

@app.get("/get_news_data")
def news_data():
    connnection = connect_to_db()
    df = get_news_data(connnection.cursor())
    return df.head(5)