from django.contrib import admin
from django.urls import path
from . import views
from . views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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
 
 #Url để gọi API, các endpoint từ đặc tả. 1 resource là 1 endpoint
    path('api/products1/', product_list, name='product_list'),
   #  path('api/products/<int:pk>/', product_detail, name='product-detail'),
   #  path('api/producttype/', producttype_list, name='producttype_list'),
   #  path('api/producttype/<int:pk>/', producttype_detail, name='producttype-detail'),
   #  path('api/customers/', customer_list, name='customer_list'),
   #  path('api/customers/<int:pk>/', customer_detail, name='customer_list'),
   #  path('api/orders/', order_list, name='product-detail'),
   #  path('api/orders/<int:pk>/', order_detail, name='product-detail'),
   #  path('api/orderitems/', orderitem_list, name='product-detail'),
   #  path('api/orderitems/<int:pk>/', orderitem_detail, name='product-detail'),
   #  path('api/suppliers/', supplier_list, name='supplier_list'),
   #  path('api/suppliers/<int:pk>/', supplier_detail, name='supplier-detail'),
   #  path('api/receipts/', receipt_list, name='receipt_list'),
   #  path('api/receipts/<int:pk>/', receipt_detail, name='receipt-detail'),
   #  path('api/receiptdetails/', receiptdetail_list, name='receipt_list'),
   #  path('api/receiptdetails/<int:pk>/', receiptdetail_detail, name='receipt-detail'),

   #-----------------------------------------------
    path('api/customers/', customer2_list, name='customer2_list'),
    path('api/products/', product2_list, name='product2_list'),
    path('api/producttype/', producttype2_list, name='producttype2_list'),
    path('api/orders/', order2_list, name='product-detail'),
    path('api/orderitems/', orderitem2_list, name='product-detail'),
    path('api/suppliers/', supplier2_list, name='supplier_list'),
    path('api/receipts/', receipt2_list, name='receipt_list'),
    path('api/receiptdetails/', receiptdetail2_list, name='receipt_list'),

    #path('api/register_1/', RegisterAPIView.as_view(), name='api_register'),
    path('api/register_2/', RegisterAPI.as_view(), name='register-api'),

    #Get user
    path('api/users/', views.UserList.as_view(), name='user-list'),
    #Get detail user, delete user
    path('api/users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    #Post user
    path('api/users/create/', views.UserCreate.as_view(), name='user-create'),
    #Put pass
    #path('api/users/<int:pk>/change-password/', views.ChangePassword.as_view(), name='change-password'),
    #path('api/users/<int:pk>/update/', views.UserUpdate.as_view(), name='user-update'),
    #Put user (cập nhật user)
    path('api/users/<int:pk>/update/', UpdateUserAPIView.as_view(), name='update_user'),
    #path('api/register_phone/', CreateUserWithPhone.as_view(), name='create_user_with_phone'),
     path('api/login/', LoginAPIView.as_view(), name='login'),
     path('api/login_1/', LoginView.as_view(), name='login_1'),
      path('api/login_2/', LoginAPIView_1.as_view(), name='login_2'),
         path('api/login_3/', LoginView_3.as_view(), name='login_3'),
   path('api/cart_0/', CartAPIView.as_view(), name='cart'),
    path('api/cart_1/', CartView.as_view(), name='cart_1'),
     path('api/cart_2/', CartView_2.as_view(), name='cart_2'),
         path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('api/order/', views.create_order, name='create_order'),
    path('api/order-item/', views.add_to_cart, name='add_to_cart'),
    path('api/cart/', views.get_cart, name='get_cart'),
      path('api/add_to_cart/', views.add_to_cart_1, name='add_to_cart_1'),
      path('api/update_order_item/<int:order_id>/item/<int:product_id>/', views.update_order_item, name='update_order_item'),
      path('api/delete_order_item/<int:order_id>/item/<int:product_id>/', views.delete_order_item, name='delete_order_item'),
      path('api/get_order/', Get_order.as_view(), name='Get_order'),
      path('api/get_orderitem/', get_orderitem.as_view(), name='get_orderitem'),
path('api/ProductSearchView/', ProductSearchView.as_view(), name='product_search_1'),
  
   
   
    
 
 #Url để gọi API, các endpoint từ đặc tả. 1 resource là 1 endpoint
    path('api/products1/', product_list, name='product_list'),
   #  path('api/products/<int:pk>/', product_detail, name='product-detail'),
   #  path('api/producttype/', producttype_list, name='producttype_list'),
   #  path('api/producttype/<int:pk>/', producttype_detail, name='producttype-detail'),
   #  path('api/customers/', customer_list, name='customer_list'),
   #  path('api/customers/<int:pk>/', customer_detail, name='customer_list'),
   #  path('api/orders/', order_list, name='product-detail'),
   #  path('api/orders/<int:pk>/', order_detail, name='product-detail'),
   #  path('api/orderitems/', orderitem_list, name='product-detail'),
   #  path('api/orderitems/<int:pk>/', orderitem_detail, name='product-detail'),
   #  path('api/suppliers/', supplier_list, name='supplier_list'),
   #  path('api/suppliers/<int:pk>/', supplier_detail, name='supplier-detail'),
   #  path('api/receipts/', receipt_list, name='receipt_list'),
   #  path('api/receipts/<int:pk>/', receipt_detail, name='receipt-detail'),
   #  path('api/receiptdetails/', receiptdetail_list, name='receipt_list'),
   #  path('api/receiptdetails/<int:pk>/', receiptdetail_detail, name='receipt-detail'),

   #-----------------------------------------------
    path('api/customers/', customer2_list, name='customer2_list'),
    path('api/products/', product2_list, name='product2_list'),
    path('api/producttype/', producttype2_list, name='producttype2_list'),
    path('api/orders/', order2_list, name='product-detail'),
    path('api/orderitems/', orderitem2_list, name='product-detail'),
    path('api/suppliers/', supplier2_list, name='supplier_list'),
    path('api/receipts/', receipt2_list, name='receipt_list'),
    path('api/receiptdetails/', receiptdetail2_list, name='receipt_list'),

    #path('api/register_1/', RegisterAPIView.as_view(), name='api_register'),
    path('api/register_2/', RegisterAPI.as_view(), name='register-api'),

    #Get user
    path('api/users/', views.UserList.as_view(), name='user-list'),
    #Get detail user, delete user
    path('api/users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    #Post user
    path('api/users/create/', views.UserCreate.as_view(), name='user-create'),
    #Put pass
    #path('api/users/<int:pk>/change-password/', views.ChangePassword.as_view(), name='change-password'),
    #path('api/users/<int:pk>/update/', views.UserUpdate.as_view(), name='user-update'),
    #Put user (cập nhật user)
    path('api/users/<int:pk>/update/', UpdateUserAPIView.as_view(), name='update_user'),
    #path('api/register_phone/', CreateUserWithPhone.as_view(), name='create_user_with_phone'),
     path('api/login/', LoginAPIView.as_view(), name='login'),
     path('api/login_1/', LoginView.as_view(), name='login_1'),
      path('api/login_2/', LoginAPIView_1.as_view(), name='login_2'),
         path('api/login_3/', LoginView_3.as_view(), name='login_3'),
   path('api/cart_0/', CartAPIView.as_view(), name='cart'),
    path('api/cart_1/', CartView.as_view(), name='cart_1'),
     path('api/cart_2/', CartView_2.as_view(), name='cart_2'),
         path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('api/order/', views.create_order, name='create_order'),
    path('api/order-item/', views.add_to_cart, name='add_to_cart'),
    path('api/cart/', views.get_cart, name='get_cart'),
      path('api/add_to_cart/', views.add_to_cart_1, name='add_to_cart_1'),
      path('api/update_order_item/<int:order_id>/item/<int:product_id>/', views.update_order_item, name='update_order_item'),
      path('api/delete_order_item/<int:order_id>/item/<int:product_id>/', views.delete_order_item, name='delete_order_item'),
      path('api/get_order/', Get_order.as_view(), name='Get_order'),
      path('api/get_orderitem/', get_orderitem.as_view(), name='get_orderitem'),
path('api/ProductSearchView/', ProductSearchView.as_view(), name='product_search_1'),
  
   
   
    
]