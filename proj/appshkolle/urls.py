from django.urls import path
from .views import ProductList, ProductDetail, ProductCreate, ProductUpdate, ProductDelete

urlpatterns = [
   path('products/', ProductList.as_view(), name='product_list'),
   path('products/<int:pk>/', ProductDetail.as_view(), name= 'product_detail'),
   path('products/create/', ProductCreate.as_view(), name='product_create'),
   path('products/<int:pk>/edit/', ProductUpdate.as_view(), name='product_update'),
   path('products/<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),

]