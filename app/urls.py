from django.urls import path, re_path
from app import views

urlpatterns = [
    re_path(r'^.*\.html', views.pages, name='pages'),
    path('pricing/', views.homepage, name='homepage'),
    path('contact/', views.contact, name='contact'),
    path('mystocks/', views.my_stocks, name='mystocks'),
    path('input/', views.input, name='input'),
    path('<int:stocks_stocks_list_id>/', views.detail, name='detail'),
    path('ai/',views.ai_methodology),
    path('',views.index,name='home'),
]
