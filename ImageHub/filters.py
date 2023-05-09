import django_filters
from .models import Image
from django import forms

class image_filter(django_filters.FilterSet):
    name=django_filters.CharFilter(lookup_expr='contains',widget=forms.TextInput(attrs={'class':'form-control tm-search-input','aria-labe':"Search",'placeholder':"Name",}))
    place=django_filters.CharFilter(lookup_expr='contains',widget=forms.TextInput(attrs={'class':'form-control tm-search-input','aria-labe':"Search",'placeholder':"Place",}))
    date=django_filters.CharFilter(lookup_expr='exact',widget=forms.DateInput(attrs={ 'type':'date','class':'form-control tm-search-input','aria-labe':"Search",'placeholder':"Date",}))

    class Meta:
        model=Image
        fields=('name','place','date')