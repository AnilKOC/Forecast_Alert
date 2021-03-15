from alpha_vantage.timeseries import TimeSeries
from .models import Asset_List,Asset_Prices
import requests
import re

def update():
    BASE = "http://127.0.0.1:5000/"
    Stocks = Asset_List.objects.all()

    for i in Stocks:
        url = i.Asset_link
        url = re.sub("https://www.investing.com/", "", url)
        url = re.sub("www.investing.com/", "", url)

        url = re.sub("/", "@", url)

        response = requests.get(BASE + "data/" + url)
        print(response.json())

    ts = TimeSeries(key='0UZLUTAJ77KHRW60', output_format='pandas')
    for i in Stocks:
        Price_history=Asset_Prices.objects.filter(asset_id=i.id).order_by('-price_date')
        data, meta_data = ts.get_daily(symbol=i.Asset_text)
        Price_first=Price_history[0].price_date[0:10]
        for j in data['4. close'].index:
            if  Price_first== str(j)[0:10]:
                break
            New_Stock_Prices = Asset_Prices(price_date=str(j), price_close=data.loc[j]['4. close'], f_day=0, s_day=0, t_day=0,asset_id=i.id)
            New_Stock_Prices.save()






