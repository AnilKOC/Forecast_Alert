from django.contrib import admin

from .models import Stock_Prices,Stocks_List

admin.site.register(Stocks_List)
admin.site.register(Stock_Prices)