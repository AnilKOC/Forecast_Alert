from django.db import models

class Stock_Type(models.Model):
    label = models.CharField(max_length=200)
    def __str__(self):
        return self.label

class Stocks_List(models.Model):
    financetype=models.ForeignKey(Stock_Type,on_delete=models.CASCADE)
    stock_text = models.CharField(max_length=200)
    f_day = models.FloatField(null=True, blank=True)
    s_day = models.FloatField(null=True, blank=True)
    t_day = models.FloatField(null=True, blank=True)
    value = models.FloatField(null=True, blank=True)
    def __str__(self):
        return self.stock_text

class Stock_Prices(models.Model):
    stocks=models.ForeignKey(Stocks_List, on_delete=models.CASCADE)
    price_date = models.CharField(max_length=200)
    price_close =models.FloatField(null=True, blank=True)
    f_day = models.FloatField(null=True, blank=True)
    s_day = models.FloatField(null=True, blank=True)
    t_day = models.FloatField(null=True, blank=True)
    def __str__(self):
        name=str(self.stocks)+str(self.price_date)
        return name

class Contact(models.Model):
    name = models.CharField(max_length=200)
    mail = models.EmailField()
    content = models.CharField(max_length=5000)
    def __str__(self):
        return self.name