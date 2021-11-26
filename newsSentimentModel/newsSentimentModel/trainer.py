"""Here we code our notebook process"""
import newsSentimentModel


df = newsSentimentModel.data.get_news_data()

#process notebook


#updating the csv_news_sentiment
newsSentimentModel.data.upload_csv_sentiment()