from django.urls import path, re_path
from app import views

urlpatterns = [
    re_path(r'^.*\.html', views.pages, name='pages'),
    path('dashboard/', views.index, name='home'),
    path('dashboard/contact/', views.contact, name='contact'),
    path('dashboard/mystocks/', views.my_stocks, name='mystocks'),
    path('dashboard/input/', views.input, name='input'),
    path('dashboard/<int:stocks_stocks_list_id>/', views.detail, name='detail'),
    path('dashboard/ai/',views.ai_methodology),
    path('',views.index,name='homepage'),
]
