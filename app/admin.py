from django.contrib import admin
from .models import Asset_Prices,Asset_List,Contact,Asset_Type

from .rmt_data import data

admin.site.site_header = "Forecast Alert"

class Asset_ListAdmin(admin.ModelAdmin):
    fields = ('financetype', 'Asset_text','Asset_link')
    def save_model(self, request, obj, form, change):
        obj.save()
        data(obj.Asset_text,obj.financetype_id,obj.id)

admin.site.register(Asset_List,Asset_ListAdmin)
admin.site.register(Asset_Prices)
admin.site.register(Asset_Type)
admin.site.register(Contact)