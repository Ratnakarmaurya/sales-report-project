from typing import KeysView
from django.shortcuts import render
from django.views.generic import ListView , DetailView
from .models import Sale
from .forms import SalesSearchForm
import pandas as pd
# Create your views here.


def home_view(request):
   sales_df = None
   form= SalesSearchForm(request.POST ,None)
   if request.method == 'POST':
      date_from  = request.POST.get('date_from')
      date_to    = request.POST.get('date_to')
      chart_type = request.POST.get('chart_type')
      print(date_from,date_to,chart_type)

      qs = Sale.objects.filter(created__date__gte = date_from, created__date__lte = date_to)
      if len(qs) > 0:
         sales_df= pd.DataFrame(qs.values())
         sales_df = sales_df.to_html()
         print(sales_df)
      else:
         print('No Data')



   context = {
      'form':form,
      'sales_df':sales_df,
   }
   return render(request,'sale/home.html',context)


# class SaleListView(ListView):
#    model = Sale
#    template_name = 'sale/main.html'

# class SaleDetail(DetailView):
#    model = Sale
#    template_name = 'sale/detail.html'

def sale_list_view(request):
   qs = Sale.objects.all()
   return render(request,'sale/main.html',{'qs':qs})

def sale_detail_view(request,**kwargs):
   pk = kwargs.get('pk')
   obj = Sale.objects.get(pk=pk)
   return render(request,'sale/detail.html',{'object':obj})


