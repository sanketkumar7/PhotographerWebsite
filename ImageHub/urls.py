from django.urls import path
from .views import *
urlpatterns = [
    path('login/',user_login_view,name='login'),
    path('logout/',user_logout_view,name='logout'),
    path('signup/',user_signup_view,name='signup'),
    path('add-image/',add_image_view,name='add_image'),
    path('display-images/',display_image_view,name='display_images'),
    path('update-image/<int:pk>',update_image_view,name='update_image'),
    path('delete-images/',delete_images_view,name='delete_images'),
    path('',image_hub_view,name='image_hub'),
    path('image-detail/<int:pk>',image_detail_view,name='image_detail')

    #path('delete-image/<int:pk>',delete_image_view,name='delete_image'),
]
