from datetime import datetime
import stockLstmModel.data
import pandas as pd

from fastapi  import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    df = stockLstmModel.data.get_stocksprice_data()
    return df.head(5)
