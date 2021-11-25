"""Here we code our notebook process"""
import news_api.data


df = news_api.data.get_news_data()

#process notebook


#updating the csv_news_sentiment
news_api.data.upload_csv_sentiment()