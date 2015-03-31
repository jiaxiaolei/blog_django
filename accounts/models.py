from django.db import models
import datetime
# Create your models here.


# 
class Pic(models.Model):
    username=models.CharField(max_length=200)
    path=models.CharField(max_length=200)
    time=models.CharField(max_length=200)
    
    
    
    
    


