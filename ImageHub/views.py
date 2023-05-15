from django.shortcuts import render,redirect
from django.core.paginator import Paginator

from django.db.models.functions import Lower

from django.views.decorators.http import require_safe

from PIL import Image as Img

from .forms import user_login_form, user_signup_form, add_image_form,update_image_form

from .models import User,Image

import os

from .filters import image_filter
# Create your views here.
def check_session(function):
    def wrapper(request, *args, **kwargs):
        if 'UserIsActive' not in request.session:
            return redirect('login') # redirect to the login page if user is not logged in
        return function(request, *args, **kwargs)
    return wrapper

def user_login_view(request):       #Login
    msg=request.GET.get('data','')
    if 'UserIsActive' in request.session:
        return redirect('add_image')
    form=user_login_form
    if request.method=='POST':
        form=user_login_form(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            request.session['UserIsActive']=username
            request.session.set_expiry(0)
            return redirect('add_image')
    return render(request,'ImageHub/login.html',{'form':form,'msg':msg})

def user_logout_view(request):
    if 'UserIsActive' in request.session:
        del request.session['UserIsActive']
        return redirect('login')

def user_signup_view(request):      #Signup
    form=user_signup_form()
    if request.method=='POST':
        form=user_signup_form(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            return redirect(f'/login?data=Registration of {username} is Successfully.')
    return render(request,'ImageHub/signup.html',{'form':form})

@require_safe
@check_session
def add_image_view(request):    #adding new Image
    msg=''
    form=add_image_form
    if request.method=='POST':
        form=add_image_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            msg=f"Image {form.cleaned_data['name']} added at {form.cleaned_data['time']} on {form.cleaned_data['date']}."
            form=add_image_form
    return render(request,'ImageHub/add_image.html',{'form':form,'msg':msg})

@require_safe
@check_session
def display_image_view(request):
    msg=request.GET.get('data','')
    #function to sort images as per requirement.
    def sorted_images(request):
        attribute=request.GET.get('attribute','')
        session_attribute=request.session.get('session_attribute','')
        sort_order=request.session.get('sort_order','desc')
            
        if attribute=='Images':
            request.session['session_attribute']=''
            sorted_images=Image.objects.all()
        elif attribute:
            if sort_order=='desc' or attribute!=session_attribute:
                sort_order='asc'
                sorted_images=Image.objects.all().order_by(Lower(attribute))
            elif sort_order=='asc':
                sort_order='desc'
                sorted_images=Image.objects.all().order_by('-'+Lower(attribute))
            request.session['sort_order']=sort_order
            request.session['session_attribute']=attribute
        else:
            if session_attribute:
                if sort_order=='asc':
                    sorted_images=Image.objects.all().order_by(Lower(session_attribute))
                else:
                    sorted_images=Image.objects.all().order_by('-'+Lower(session_attribute))
            else:
                sorted_images=Image.objects.all()
        return sorted_images
    images=sorted_images(request)
    myfilter=image_filter(request.GET,queryset=images)
    if len(myfilter.qs)!=0 and len(images)!=len(myfilter.qs):
        images=myfilter.qs
        paginator = Paginator(images, len(myfilter.qs)+5)
    else:
        images=myfilter.qs
        paginator = Paginator(images,10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    srno=(int(page_number)-1)*10    # use to forward srno
    return render(request,'ImageHub/display_image.html',{'page':page,'msg':msg,'myfilter':myfilter,'srno':srno})

@require_safe
@check_session
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
            return redirect(f'/display-images?data={image.name}({pk}) Updated.')
    return render(request,'ImageHub/update_image.html',{'form':form})

@require_safe
@check_session
def delete_images_view(request):        #deleting multiple images.
    data=[]
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items')
        if selected_items:
            for pk in map(int,selected_items):
                image=Image.objects.get(pk=pk)
                image_name=image.name
                image_path=image.image.path
                image.delete()
                os.remove(image_path)
                data.append(f'{image_name}({pk})')
    if data:
        return redirect(f'/display-images?data=Item - '+(', ').join(data)+' Deleted.')
    return redirect(f'/display-images?data=0 Items '+(', ').join(data)+' Deleted.')

@require_safe
def image_hub_view(request):
    images=Image.objects.all().order_by('-date','-time')
    myfilter=image_filter(request.GET,queryset=images)
    if len(myfilter.qs)!=0 and len(images)!=len(myfilter.qs):
        images=myfilter.qs
        paginator = Paginator(images, len(myfilter.qs)+5)
    else:
        images=myfilter.qs
        paginator = Paginator(images,12)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    return render(request,'ImageHub/image_hub.html',{'page':page,'myfilter':myfilter})

@require_safe
def image_detail_view(request,pk):
    image_obj=Image.objects.get(pk=pk)
    image_obj.views+=1
    image_obj.save()
    PIL_image=Img.open(image_obj.image.path)
    images=Image.objects.filter(name__contains=image_obj.name).exclude(pk=pk)
    if images.exists() is not True:
        images=Image.objects.filter(date__gte=image_obj.date).exclude(pk=pk)
    paginator = Paginator(images, 4)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    context={
        'image_obj':image_obj,
        'PIL_image':PIL_image,
        'page':page,
    }
    return render(request,'ImageHub/image_detail.html',context=context)

'''def delete_image_view(request,pk):      #deleting image
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
    return redirect(f'/display-image?data={image.name}({pk}) Deleted.')'''
    