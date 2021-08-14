from django.db import models
from django.db.models.base import Model
from product.models import Product
from customers.models import Customers
from profiles.models import Profile
from django.utils import timezone 
from django.urls import reverse
from .utils import generate_code
# Create your models here.
class Position(models.Model):
   product  = models.ForeignKey(Product , on_delete=models.CASCADE)
   quantity = models.PositiveIntegerField()
   price    = models.FloatField(blank=True)
   created  = models.DateTimeField(blank=True)

   def save(self , *args , **kwargs):
      self.price = self.product.price * self.quantity
      return super().save(*args ,**kwargs)

   def get_sale_id(self):
      sale_obj = self.sale_set.first()
      return sale_obj.id

   def __str__(self):
      return f"id:{self.id}, product:{self.product.name}, quantity:{self.quantity}"




class Sale(models.Model):
   transaction_id = models.CharField(max_length=12,blank=True)
   position       = models.ManyToManyField(Position)
   total_price    = models.FloatField(blank=True ,null=True)
   customer       = models.ForeignKey(Customers ,on_delete=models.CASCADE)
   salesman       = models.ForeignKey(Profile,on_delete=models.CASCADE)
   created        = models.DateTimeField(blank=True)
   updated        = models.DateTimeField(auto_now=True)

   def save (self , *args , **kwargs):
      if self.transaction_id == "":
         self.transaction_id = generate_code()
      if self.created is None:
         self.created = timezone.now()
      return super().save(*args ,**kwargs)

   def __str__(self):
      return f"Sales for the amount of RS:{self.total_price}"

   def get_absolute_url(self):
       return reverse("sale:detail", kwargs={"pk": self.pk})
   
   def get_position(self):
      return self.position.all()

class CSV(models.Model):
   file_name = models.FileField(upload_to='csvs')
   activated = models.BooleanField(default=False)
   created   = models.DateTimeField(auto_now_add=True)
   updated   = models.DateTimeField(auto_now=True)

   def __str__(self):
      return f"{self.file_name}"