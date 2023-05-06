from django.shortcuts import render,redirect
from django.http import HttpResponse

from .forms import user_login_form, user_signup_form, add_image_form,update_image_form

from .models import User,Image

import os,time
# Create your views here.
def user_login_view(request):       #Login
    form=user_login_form
    if request.method=='POST':
        form=user_login_form(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            if User.objects.filter(username=username,password=password).exists():
                return redirect('add_image')
            else:
                return HttpResponse('Failed')
    return render(request,'ImageHub/login.html',{'form':form})
def user_signup_view(request):      #Signup
    form=user_signup_form()
    if request.method=='POST':
        form=user_signup_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request,'ImageHub/signup.html',{'form':form})

def add_image_view(request):    #adding new Image
    form=add_image_form
    if request.method=='POST':
        form=add_image_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("<h1>SUCCESS</h1>")
    return render(request,'ImageHub/add_image.html',{'form':form})

def display_image_view(request):
    msg=request.GET.get('data','')
    print(msg)
    images=Image.objects.all()
    return render(request,'ImageHub/display_image.html',{'images':images,'msg':msg})

def update_image_view(request,pk):
    image=Image.objects.get(pk=pk)
    form=update_image_form(instance=image)
    if request.method=='POST':
        old_image_path=image.image.path
        form=update_image_form(request.POST,request.FILES,instance=image)
        if form.is_valid():
            form.save(commit=True)
            new_image_path=image.image.path
            if old_image_path!=new_image_path:
                os.remove(old_image_path)
            return redirect(f'/display-image?data={image.name}({pk}) Updated.')
    return render(request,'ImageHub/update_image.html',{'form':form})

def delete_image_view(request,pk):      #deleting images
    try:
        image=Image.objects.get(pk=pk)
        image_name=image.name
        image_path=image.image.path
        image.delete()
        os.remove(image_path)
    except Image.DoesNotExist :
        pass
    except Exception as e:
        print(e)
    return redirect(f'/display-image?data={image.name}({pk}) Deleted.')