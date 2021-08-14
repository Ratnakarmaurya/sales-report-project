from django.urls import path
from django.urls.resolvers import URLPattern
from .views import (home_view,sale_detail_view ,sale_list_view)

app_name ='sale'

urlpatterns =[
   path('',home_view, name='home'),
   path('sale/',sale_list_view, name='list'),
   path('sale/<pk>/',sale_detail_view, name='detail'),
]