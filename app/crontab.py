from alpha_vantage.timeseries import TimeSeries
from .models import Stocks_List,Stock_Prices

def update():
    Stocks = Stocks_List.objects.all()
    ts = TimeSeries(key='0UZLUTAJ77KHRW60', output_format='pandas')
    for i in Stocks:
        Price_history=Stock_Prices.objects.filter(stocks_id=i.id).order_by('-price_date')
        data, meta_data = ts.get_daily(symbol=i.stock_text)
        Price_first=Price_history[0].price_date[0:10]
        for j in data['4. close'].index:
            if  Price_first== str(j)[0:10]:
                break
            New_Stock_Prices = Stock_Prices(price_date=str(j), price_close=data.loc[j]['4. close'], f_day=0, s_day=0, t_day=0,stocks_id=i.id)
            New_Stock_Prices.save()




