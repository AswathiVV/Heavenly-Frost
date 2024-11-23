from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Cake(models.Model):
    cake_id=models.TextField()
    cake_name=models.TextField()
    price=models.IntegerField()
    img=models.FileField()
    category=models.TextField()
    colour=models.TextField()
    quantity=models.IntegerField()
    description=models.TextField()

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cake=models.ForeignKey(Cake,on_delete=models.CASCADE)   

class Buy(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cake=models.ForeignKey(Cake,on_delete=models.CASCADE)
    price=models.IntegerField()
    date=models.DateField(auto_now_add=True)      