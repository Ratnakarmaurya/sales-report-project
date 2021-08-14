from typing import KeysView
from django.shortcuts import render
from django.views.generic import ListView , DetailView
from .models import Sale
from .forms import SalesSearchForm
# Create your views here.


def home_view(request):
   form= SalesSearchForm(request.POST ,None)
   if request.method == 'POST':
      date_from  = request.POST.get('date_from')
      date_to    = request.POST.get('date_to')
      chart_type = request.POST.get('chart_type')
      print(date_from,date_to,chart_type)
      
   context = {
      'form':form,
   }
   return render(request,'sale/home.html',context)


class SaleListView(ListView):
   model = Sale
   template_name = 'sale/main.html'

class SaleDetail(DetailView):
   model = Sale
   template_name = 'sale/detail.html'

def sale_list_view(request):
   qs = Sale.objects.all()
   return render(request,'sale/main.html',{'qs':qs})

def sale_detail_view(request,**kwargs):
   pk = kwargs.get('pk')
   obj = Sale.objects.get(pk=pk)
   return render(request,'sale/detail.html',{'object':obj})


