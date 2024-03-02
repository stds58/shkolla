from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Author,Product,UserProduct,Group,UserGroup,Videos,Lesson,VideosLesson
from django.utils import timezone
from .forms import ProductForm
from django.urls import reverse_lazy



class ProductList(ListView):
    model = Product
    ordering = '-datestart'
    #queryset = Product.objects.filter(datestart__gte=timezone.now()).order_by('-datestart')
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 10


class ProductDetail(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product_detail'


class ProductCreate(CreateView):
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'


class ProductUpdate(UpdateView):
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'


class ProductDelete(DeleteView):
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')