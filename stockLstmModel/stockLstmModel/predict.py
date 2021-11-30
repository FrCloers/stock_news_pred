from .data import upload_LSTM_prediction


df_to_update = model.joblib(df)



if __name__ == "__main__":
    upload_LSTM_prediction(df_to_update)