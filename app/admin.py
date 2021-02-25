from django.contrib import admin
from .models import Stock_Prices,Stocks_List,Contact,Stock_Type

from .rmt_data import data

admin.site.site_header = "Forecast Alert"

class Stock_ListAdmin(admin.ModelAdmin):
    fields = ('financetype', 'stock_text')
    def save_model(self, request, obj, form, change):
        obj.save()
        data(obj.stock_text,obj.financetype_id,obj.id)

admin.site.register(Stocks_List,Stock_ListAdmin)
admin.site.register(Stock_Prices)
admin.site.register(Stock_Type)
admin.site.register(Contact)