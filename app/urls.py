from django.contrib import admin
from django.urls import path
from . import views
from . views import *

urlpatterns = [
    #Link cũ ko xài
    path('',views.home, name="home"),
    path('cart/',views.cart, name="cart"),
    path('checkout/',views.checkout, name="checkout"),
    path('update_item/',views.updateItem, name="update_item"),
    path('register/',views.register, name="register"),
    path('login/',views.loginPage, name="login"),
    path('logout/',views.logoutPage, name="logout"),
    path('search/',views.search, name="search"),
 
 #Url để gọi API
    path('api/products/', product_list, name='product_list'),
    path('api/products/<int:pk>/', product_detail, name='product-detail'),
    path('api/producttype/', producttype_list, name='producttype_list'),
    path('api/producttype/<int:pk>/', producttype_detail, name='producttype-detail'),
    path('api/customers/', customer_list, name='customer_list'),
    path('api/customers/<int:pk>/', customer_detail, name='customer_list'),
    path('api/orders/', order_list, name='product-detail'),
    path('api/orders/<int:pk>/', order_detail, name='product-detail'),
    path('api/orderitems/', orderitem_list, name='product-detail'),
    path('api/orderitems/<int:pk>/', orderitem_detail, name='product-detail'),
    path('api/suppliers/', supplier_list, name='supplier_list'),
    path('api/suppliers/<int:pk>/', supplier_detail, name='supplier-detail'),
    path('api/receipts/', receipt_list, name='receipt_list'),
    path('api/receipts/<int:pk>/', receipt_detail, name='receipt-detail'),
    path('api/receiptdetails/', receiptdetail_list, name='receipt_list'),
    path('api/receiptdetails/<int:pk>/', receiptdetail_detail, name='receipt-detail'),

    #path('api/register_1/', RegisterAPIView.as_view(), name='api_register'),
    #path('api/register_2/', RegisterAPI.as_view(), name='register-api'),

    #Get user
    path('api/users/', views.UserList.as_view(), name='user-list'),
    #Get user, Put user, delete user
    path('api/users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    #Post user
    path('api/users/create/', views.UserCreate.as_view(), name='user-create'),
    #Put pass
    path('api/users/<int:pk>/change-password/', views.ChangePassword.as_view(), name='change-password'),
    #path('api/users/<int:pk>/update/', views.UserUpdate.as_view(), name='user-update'),
    #Put user (cập nhật user)
    path('api/users/<int:pk>/update/', UpdateUserAPIView.as_view(), name='update_user'),
    path('api/register_phone/', CreateUserWithPhone.as_view(), name='create_user_with_phone'),
     path('api/login/', LoginAPIView.as_view(), name='login'),
    
]