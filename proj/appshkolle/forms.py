from django import forms
from .models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['nameprod', 'datestart', 'price', 'kolvomin', 'kolvomax', 'user']
        labels = {
            'nameprod': 'название',
            'datestart': 'дата_начала',
            'price': 'стоимость',
            'kolvomin': 'наим_колво_в_группе',
            'kolvomax': 'наиб_колво_в_группе',
            'user': 'препод'
        }

