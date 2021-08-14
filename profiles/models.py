from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.
class Profile(models.Model):
   user     = models.OneToOneField(User,on_delete=CASCADE)
   bio      = models.TextField(default= 'no bio..')
   avatar   = models.ImageField(upload_to='avatars',default='no_pitcure.png')
   created  = models.DateTimeField(auto_now_add=True)
   updated  = models.DateTimeField(auto_now=True)

   def __str__(self):
      return f"Profile of {self.user.username}"
