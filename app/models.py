from django.db import models

class Stocks_List(models.Model):
    stock_text = models.CharField(max_length=200)
    f_day = models.FloatField()
    s_day = models.FloatField()
    t_day = models.FloatField()
    value = models.FloatField()
    def __str__(self):
        return self.stock_text

class Stock_Prices(models.Model):
    stocks=models.ForeignKey(Stocks_List, on_delete=models.CASCADE)
    price_date = models.CharField(max_length=200)
    price_close =models.FloatField()
    f_day = models.FloatField()
    s_day = models.FloatField()
    t_day = models.FloatField()
    def __str__(self):
        name=str(self.stocks)+str(self.price_date)
        return name

class Contact(models.Model):
    name = models.CharField(max_length=200)
    mail = models.EmailField()
    content = models.CharField(max_length=5000)
    def __str__(self):
        return self.name