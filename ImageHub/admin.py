from django.contrib import admin
from .models import User,Image
# Register your models here.
class user_admin(admin.ModelAdmin):
    list_display=['username','first_name','last_name','password']

class image_admin(admin.ModelAdmin):
    list_display=['name','time','date','place','image']
    
admin.site.register(User,user_admin)
admin.site.register(Image,image_admin)