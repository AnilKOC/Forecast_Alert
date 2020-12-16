from alpha_vantage.timeseries import TimeSeries
from django.db import connection
import math
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import Dense,LSTM


def prediction(data):
    dataset = pd.DataFrame(data)
    training_data_len = math.ceil(len(dataset) * 0.95)

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)

    train_data = scaled_data[0:training_data_len, :]

    x_train = []
    y_train = []

    for i in range(60, len(train_data)):
        x_train.append(train_data[i - 60:i, 0])
        y_train.append(train_data[i, 0])
        if i <= 60:
            print(x_train)
            print()
            print(y_train)

    x_train, y_train = np.array(x_train), np.array(y_train)

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    model = Sequential()

    model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(x_train, y_train, batch_size=10, epochs=1)
    test_data = scaled_data[training_data_len - 60:, :]

    valid = dataset[training_data_len:training_data_len + 1]

    x_test = []
    x_test.append(test_data[0:60, 0])
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    predictions = model.predict(x_test)
    f_day = scaler.inverse_transform(predictions)

    valid['24 Hour'] = f_day

    x_test = []
    x_test.append(test_data[1:60, 0])
    x_test[0] = x_test[0].tolist()
    x_test[0].append(predictions[0][0])
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    predictions2 = model.predict(x_test)
    s_day = scaler.inverse_transform(predictions2)

    valid['48 Hour'] = s_day

    x_test = []
    x_test.append(test_data[2:60, 0])
    x_test[0] = x_test[0].tolist()
    x_test[0].append(predictions[0][0])
    x_test[0].append(predictions2[0][0])
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    predictions3 = model.predict(x_test)
    t_day = scaler.inverse_transform(predictions3)

    valid['72 Hour'] = t_day
    cursor = connection.cursor()
    sql = "UPDATE app_stocks_list SET f_day=%s, s_day=%s, t_day=%s WHERE id=%s"
    val= (round(float(f_day),0),round(float(s_day),2),round(float(t_day),2),50)
    cursor.execute(sql,val)
    return valid


def data(ticker):
    ts = TimeSeries(key='0UZLUTAJ77KHRW60', output_format='pandas')
    data, meta_data = ts.get_daily(symbol=ticker)
    data_insert(ticker,data['4. close'],list(data.index.values))
    prediction(data['4. close'])

def data_insert(ticker,data,index):
    cursor = connection.cursor()
    sql="INSERT INTO app_stocks_list (stock_text,f_day,s_day,t_day,value) VALUES(%s,%s,%s,%s,%s)"
    val=(ticker,0,0,0,data[0])
    cursor.execute(sql, val)
    a=cursor.execute("Select id from app_stocks_list where stock_text = '"+ticker+"'")
    print(a)#+25 sonra silinicek veri tabanı id lemesi yüzünden yazıldı.
    sql="INSERT INTO app_stock_prices (price_date,price_close,f_day,s_day,t_day,stocks_id) VALUES(%s,%s,%s,%s,%s,%s)"
    for i in range(len(data)):
        val=(index[i],data[i],50,50,50,50)
        cursor.execute(sql, val)

