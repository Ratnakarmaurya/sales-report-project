from django.shortcuts import render
from django.views.generic import ListView , DetailView
from pandas.core.arrays.integer import safe_cast
from .models import Position, Sale
from .forms import SalesSearchForm
import pandas as pd
from .utils import get_customer_by_id,get_salesman_by_id
# Create your views here.


def home_view(request):
   sales_df    = None
   position_df = None
   merged_df   = None
   form= SalesSearchForm(request.POST ,None)
   if request.method == 'POST':
      date_from  = request.POST.get('date_from')
      date_to    = request.POST.get('date_to')
      chart_type = request.POST.get('chart_type')

      sales_qs = Sale.objects.filter(created__date__gte = date_from, created__date__lte = date_to)
   
      if len(sales_qs) > 0:
         sales_df= pd.DataFrame(sales_qs.values())
         sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_by_id)
         sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_by_id)
         sales_df = sales_df.rename({'customer_id': 'customer','s;alesman_id':'salesman','id':'sales_id'},axis=1)
         sales_df['created'] = sales_df['created'].apply(lambda _ : _.strftime('%Y-%m-%d'))
         sales_df['updated'] = sales_df['updated'].apply(lambda _ : _.strftime('%Y-%m-%d'))
         position_data = []
         for sale in sales_qs:
            for pos in sale.get_position():
               obj = {
                  'position_id':pos.id,
                  'product_name':pos.product.name,
                  'quantity': pos.quantity,
                  'price':pos.price,
                  'sales_id':pos.get_sale_id(),
               }
               position_data.append(obj)
         
         position_df = pd.DataFrame(position_data)
         merged_df = pd.merge(sales_df,position_df, on='sales_id')
         # print(position_df)
         sales_df    = sales_df.to_html()
         position_df = position_df.to_html()
         merged_df   = merged_df.to_html()

         print(sales_df)
      else:
         print('No Data')



   context = {
      'form':form,
      'sales_df':sales_df,
      'position_df':position_df,
      'merged_df': merged_df,
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


