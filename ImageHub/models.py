from django.db import models
from django.utils.timezone import now
# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=200)
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
class Image(models.Model):
    name = models.CharField(max_length=255)
    time = models.TimeField(default=now().time())
    date = models.DateField(default=now().date()) 
    place = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name