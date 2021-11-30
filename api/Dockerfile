FROM python:3.8.12-buster


COPY . .
COPY ../newsSentimentModel/newsSentimentModel newsSentimentModel
COPY ../stockLstmModel/stockLstmModel stockLstmModel
COPY ../tweetSentimentModel/tweetSentimentModel tweetSentimentModel
COPY ../stockSentimentModel/stockSentimentModel stockSentimentModel

RUN pip install -U pip
RUN pip install fastapi uvicorn
RUN pip install -e .


CMD uvicorn fast:app --host 0.0.0.0 --port $PORT