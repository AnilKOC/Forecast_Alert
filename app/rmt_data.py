from alpha_vantage.timeseries import TimeSeries
from django.db import connection
import math
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense,LSTM
from .models import Stocks_List,Stock_Prices

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

    Stock=Stocks_List.objects.last()
    Stock.f_day=round(float(f_day))
    Stock.s_day=round(float(s_day))
    Stock.t_day=round(float(t_day))
    Stock.save()
    return valid

def data(ticker):
    ts = TimeSeries(key='0UZLUTAJ77KHRW60', output_format='pandas')
    data, meta_data = ts.get_daily(symbol=ticker)
    data_insert(ticker,data['4. close'],list(data.index.values))
    prediction(data['4. close'])

def data_insert(ticker,data,index):
    New_Stock=Stocks_List(stock_text=ticker,f_day=0,s_day=0,t_day=0,value=data[0])
    New_Stock.save()
    for i in range(len(data)):
        New_Stock_Prices=Stock_Prices(price_date=index[i],price_close=data[i],f_day=0,s_day=0,t_day=0,stocks_id=New_Stock.id)
        New_Stock_Prices.save()
