from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django import template
from django.contrib.auth.decorators import user_passes_test

from django.core import serializers

from .models import Asset_List,Asset_Prices, Asset_Type
from .rmt_data import data
from .forms import Contact_form
from .models import Contact
from .crontab import update

def homepage(request):
    return render(request,'homepage.html')

@login_required(login_url="/login/")
def index(request):
    Stocks =Asset_List.objects.all()
    #Stocks = serializers.serialize('json', Stocks)
    Type = Asset_Type.objects.all()
    #Type = serializers.serialize('json', Type)
    context = {'Stocks': Stocks,
               'Type':Type,
               }
    return render(request, 'index.html', context)

@login_required(login_url="/login/")
def ai_methodology(request):
    return render(request,'ai-methodology.html')

@login_required(login_url="/login/")
def contact(request):
    if request.method == 'POST':
        form = Contact_form(request.POST)
        if form.is_valid():
            print(form)
            cont=Contact(name=form.cleaned_data['name'],mail=form.cleaned_data['mail'],content=form.cleaned_data['message'])
            cont.save()
            return render(request, 'contact.html', {'form': form})
    else:
        form = Contact_form()
    return render(request, 'contact.html', {'form': form})

@login_required(login_url="/login/")
def my_stocks(request):
    Stocks = Asset_List.objects.all()
    context = {'Stocks': Stocks}
    if request.method == 'POST':
        print(request.POST) #askıya kaldırıldı şimdilik.
    return render(request, 'stock.html', context)

@user_passes_test(lambda u: u.is_superuser) #crontab
def input(request):
    if request.method == 'POST':
        update()
        return render(request,'input.html')
    return render(request,'input.html')

@login_required(login_url="/login/")
def detail(request, stocks_stocks_list_id):
    stock_list = Asset_Prices.objects.filter(asset_id=stocks_stocks_list_id).order_by('-price_date')
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
