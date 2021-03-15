from alpha_vantage.timeseries import TimeSeries
from django.db import connection
import math
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense,LSTM
from .models import Asset_List,Asset_Prices

from tensorflow import keras

def prediction(data):
    final_model = keras.models.load_model('final_model')

    data = data.iloc[::-1]

    dataset = pd.DataFrame(data)

    training_data_len = math.ceil(len(dataset) * 0.8)

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)

    test_data = scaled_data[training_data_len - 14:, :]

    x_test = []

    x_test.append(test_data[-14:, 0])

    x_test = np.array(x_test)

    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    predictions = final_model.predict(x_test)
    f_day = scaler.inverse_transform(predictions)

    test_data = np.append(test_data, predictions[0])

    x_test = []
    x_test.append(test_data[-14:])

    x_test = np.array(x_test)

    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    print(x_test)
    predictions = final_model.predict(x_test)
    s_day = scaler.inverse_transform(predictions)

    test_data = np.append(test_data, predictions[0])

    x_test = []
    x_test.append(test_data[-14:])

    x_test = np.array(x_test)

    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    print(x_test)
    predictions = final_model.predict(x_test)
    t_day = scaler.inverse_transform(predictions)

    print(f_day[0][0], s_day[0][0], t_day[0][0])

    Asset=Asset_List.objects.last()
    Asset.value=data[-1]
    Asset.f_day=format(f_day[0][0],'.2f')
    Asset.s_day=format(s_day[0][0],'.2f')
    Asset.t_day=format(t_day[0][0],'.2f')
    Asset.save()

def data(ticker,fin_id,id):
    ts = TimeSeries(key='0UZLUTAJ77KHRW60', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=ticker,interval='60min', outputsize='full')
    data_insert(ticker,data['4. close'],list(data.index.values),fin_id,id)
    prediction(data['4. close'])

def data_insert(ticker,data,index,fin_id,id):
    for i in range(len(data)):
        New_Stock_Prices=Asset_Prices(price_date=index[i],price_close=data[i],f_day=0,s_day=0,t_day=0,asset_id=id)
        New_Stock_Prices.save()
