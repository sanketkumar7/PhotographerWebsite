from django import forms
from .models import User,Image

from datetime import datetime
'''login form'''
class user_login_form(forms.ModelForm):
    '''Fields definition'''
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    '''login form Validation'''
    def clean(self):
        cleaned_data=super().clean()
        return cleaned_data
    class Meta:
        model=User
        fields=('username','password')  # required fields
'''Signup form'''
class user_signup_form(forms.ModelForm):
    '''Field definition'''
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    '''signup form Validation'''
    def clean(self):
        cleaned_data=super().clean()
        return cleaned_data
    class Meta:
        model=User
        fields='__all__'        # required fields
'''Image form'''
class add_image_form(forms.ModelForm):
    '''Field definitions'''
    name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    time=forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control'}),initial=datetime.now())
    date=forms.DateField(widget=forms.DateInput(attrs={'type':'date','class':'form-control'}),initial=datetime.now())
    place=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    image=forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control'}))
    '''Image validation'''
    def clean(self):
        cleaned_data=super().clean()
        return cleaned_data
    
    class Meta:
        model=Image
        fields=('name','time','date','place','image')

    '''Update Image Form'''
class update_image_form(forms.ModelForm):
    '''Field definitions'''
    name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    time=forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control'}))
    date=forms.DateField(widget=forms.DateInput(attrs={'type':'date','class':'form-control'}),label='Old Date')
    place=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    image=forms.ImageField()
    '''Image validation'''
    def clean(self):
        cleaned_data=super().clean()
        return cleaned_data
    
    class Meta:
        model=Image
        fields=('name','time','date','place','image')
