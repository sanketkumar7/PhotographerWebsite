from django.db import models
from django.core.validators import FileExtensionValidator,RegexValidator
from .validators import MaxFileSizeValidator,MinFileSizeValidator
from django.utils.timezone import now
# Create your models here.
msg={
    'username_msg':'1.At least one alphabet\n 2.At least one numeric value\n 3.Allowed size 5 to 15 character',
    'name_msg':'Only alphabets are allowed to set Name.'
}
class User(models.Model):
    username=models.CharField(max_length=200,validators=[RegexValidator('^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{5,15}$',message=msg['username_msg'])])
    first_name=models.CharField(max_length=200,validators=[RegexValidator('[a-zA-Z]+$',message=msg['name_msg'])])
    last_name=models.CharField(max_length=200,validators=[RegexValidator('[a-zA-Z]+$',message=msg['name_msg'])])
    master_key=models.CharField(max_length=200,default=None)
    password=models.CharField(max_length=200)

def image_upload_path(instance, filename):
    extension = filename.split('.')[-1]
    filename = f"{instance.name}-{instance.time}-{instance.date}.{extension}".replace(':', '')
    return f"images/{filename}"

class Image(models.Model):
    name = models.CharField(max_length=255,validators=[RegexValidator('^[\w\s]{2,}$',message='Only alphanumeric values are allowed.')])
    time = models.TimeField(default=now().time())
    date = models.DateField(default=now().date()) 
    place = models.CharField(max_length=255,validators=[RegexValidator('^(?=.*[A-Za-z]{3})[A-Za-z0-9]{3,30}$',message='Only alphanumeric values are allowed.')])
    image = models.ImageField(upload_to=image_upload_path,validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png']),MinFileSizeValidator(1024*10,message='File size should be at least 10kb'),MaxFileSizeValidator(1024*1024*10,message='File size should not exceed 10mb.')])
    views=models.IntegerField(default=0)
    def __str__(self):
        return self.name