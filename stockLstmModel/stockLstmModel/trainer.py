"""Here we code our notebook process to traine the LSTM"""
from pymysql import cursors
from stockLstmModel.data import get_stocksprice_data, upload_LSTM_prediction, connect_to_db
from stockLstmModel.utils import simple_time_tracker

@simple_time_tracker
def save_model():
    #function pour enregister model.joblib
    pass



if __name__ == "__main__":
    connection = connect_to_db()
    cursors = connection.cursor()

    df = get_stocksprice_data(cursors, 'AMZN')
    print(df.head(5))
    




