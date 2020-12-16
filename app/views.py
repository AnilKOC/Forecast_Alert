from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from .models import Stocks_List,Stock_Prices
from django.contrib.auth.decorators import user_passes_test

from .rmt_data import data

@login_required(login_url="/login/")
def index(request):
    Stocks = Stocks_List.objects.all()
    context = {'Stocks': Stocks}
    return render(request, 'index.html', context)

@login_required(login_url="/login/")
def my_stocks(request):
    Stocks = Stocks_List.objects.all()
    context = {'Stocks': Stocks}
    if request.method == 'POST':
        print(request.POST)
    return render(request, 'stock.html', context)

@user_passes_test(lambda u: u.is_superuser)
def input(request):
    if request.method == 'POST':
        context = request.POST
        data(context['ticker'])
        return render(request,'input.html')
    return render(request,'input.html')

@login_required(login_url="/login/")
def detail(request, stocks_stocks_list_id):
    stock_list = Stock_Prices.objects.filter(stocks_id=stocks_stocks_list_id)
    return render(request, 'detail.html', {'stock_list': stock_list})


@login_required(login_url="/login/")
def pages(request):
    context = {}
    try:
        load_template = request.path.split('/')[-1]
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template( 'error-404.html' )
        return HttpResponse(html_template.render(context, request))
    except:
        html_template = loader.get_template( 'error-500.html' )
        return HttpResponse(html_template.render(context, request))
