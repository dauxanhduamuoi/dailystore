from django.contrib import admin
from django.urls import path
from . import views
from . views import *

urlpatterns = [
    path('',views.home, name="home"),
    path('cart/',views.cart, name="cart"),
    path('checkout/',views.checkout, name="checkout"),
    path('update_item/',views.updateItem, name="update_item"),
    path('register/',views.register, name="register"),
    path('login/',views.loginPage, name="login"),
    path('logout/',views.logoutPage, name="logout"),
    path('search/',views.search, name="search"),
    path('api/products/', product_list, name='product_list'),
    path('api/products/<int:pk>/', product_detail, name='product-detail'),
    path('api/producttype/', producttype_list, name='producttype_list'),
    path('api/producttype/<int:pk>/', producttype_detail, name='producttype-detail'),
    path('api/customers/', customer_list, name='customer_list'),
    path('api/products/<int:pk>/', product_detail, name='product-detail'),
    path('api/suppliers/', supplier_list, name='supplier_list'),
    path('api/suppliers/<int:pk>/', supplier_detail, name='supplier-detail'),
]