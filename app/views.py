from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from . models import * 
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .serializers import * #import from serializers.py
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.
def search(request):
    if request.method =="POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains = searched)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        # order = {'order.get_cart_items':0,'order.get_cart_total' : 0}
        order = {'get_cart_items':0,'get_cart_total' : 0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    context={'products': products,'cartItems':cartItems}
    return render(request, 'app/search.html',{"searched": searched,"keys":keys,'products': products,'cartItems':cartItems})
    return render(request,'app/search.html')
def register(request):
    form =CreateUserForm()
    user_login = 'hidden'
    user_not_login ='hidden'
    search_bar = 'hidden'
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            #a=request.POST.get('username')
            form.save()
            user = form.save()
            user.is_staff = True  # Set is_staff to True
            user.save()  # Save the updated user object


            Customer.objects.create(
                user=user,
                name=user.first_name + " " + user.last_name,  # Or however you want to set the name
                email=user.email
            )
        user_login = 'hidden'
        user_not_login ='hidden'
        search_bar = 'hidden'
        return redirect('login')
    context={'form':form,'user_login':user_login,'user_not_login':user_not_login,'search_bar':search_bar}
    return render(request,'app/register.html',context)
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect("home")
        else: messages.info(request,'user or password not correct!')
    context={}
    return render(request,'app/login.html',context)
def logoutPage(request):
    logout(request)
    return redirect('login')
def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_login = 'show'
        user_not_login ='hidden'
    else:
        items = []
        # order = {'order.get_cart_items':0,'order.get_cart_total' : 0}
        order = {'get_cart_items':0,'get_cart_total' : 0}
        cartItems = order['get_cart_items']
        user_login = 'hidden'
        user_not_login ='show'
    products = Product.objects.all()
    context={'products': products,'cartItems':cartItems,'user_login':user_login,'user_not_login':user_not_login}
    return render(request, 'app/home.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_login = 'show'
        user_not_login ='hidden'
    else:
        items = []
        # order = {'order.get_cart_items':0,'order.get_cart_total' : 0}
        order = {'order.get_cart_items':0,'order.get_cart_total' : 0}
        cartItems = order['get_cart_item']
        user_login = 'hidden'
        user_not_login ='show'

    context={'items':items,'order':order,'cartItems':cartItems,'user_login':user_login,'user_not_login':user_not_login}
    return render(request, 'app/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_login = 'show'
        user_not_login ='hidden'
    else:
        items = []
        # order = {'order.get_cart_items':0,'order.get_cart_total' : 0}
        order = {'get_cart_items':0,'get_cart_total' : 0}
        cartItems = order['get_cart_item']
        user_login = 'hidden'
        user_not_login ='show'
    context={'items':items,'order':order,'cartItems':cartItems,'user_login':user_login,'user_not_login':user_not_login}
    return render(request, 'app/checkout.html', context)

def updateItem (request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id = productId)
    order, create = Order.objects.get_or_create(customer = customer, complete = False)
    orderItem, create = OrderItem.objects.get_or_create(order = order, product = product)
    if action =='add':  
        orderItem.quantity += 1
    elif action =='remove':
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('added',safe=False)
#------------------------------------------------------------------------------------
#Product
@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def product_list(request):
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#------------------------------------------------------------------------------------
#ProductType
@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def producttype_list(request):
    if request.method == "GET":
        products_type = ProductType.objects.all()
        serializer = ProductTypeSerializer(products_type, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ProductTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def producttype_detail(request, pk):
    try:
        product_type = ProductType.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProductTypeSerializer(product_type)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductTypeSerializer(product_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        product_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#------------------------------------------------------------------------------------
#Customer
@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def customer_list(request):
    if request.method == "GET":
        customer = Customer.objects.all()
        serializer = CustomerSerializer(customer, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#------------------------------------------------------------------------------------
#Supplier
@api_view(['GET', 'POST'])
#@parser_classes([MultiPartParser, FormParser])
def supplier_list(request):
    if request.method == "GET":
        supplier = Supplier.objects.all()
        serializer = SupplierSerializer(supplier, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def supplier_detail(request, pk):
    try:
        supplier = Supplier.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SupplierSerializer(supplier, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        supplier.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    

#------------------------------------------------------------------------------------
#Register
@api_view(['POST'])
def register_api(request):
    if request.method == "POST":
        form = CreateUserForm(request.data)  # Sử dụng request.data thay vì request.POST
        
        if form.is_valid():
            # Lưu user
            user = form.save()
            user.is_staff = True
            user.save()
            
            # Tạo customer
            Customer.objects.create(
                user=user,
                name=user.first_name + " " + user.last_name,
                email=user.email
            )
            
            # Trả về response thành công
            return Response({
                'message': 'User registered successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            }, status=status.HTTP_201_CREATED)
        
        # Nếu form không valid, trả về lỗi
        return Response({
            'errors': form.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Nếu không phải POST request
    return Response({
        'error': 'Method not allowed'
    }, status=status.HTTP_405_METHOD_NOT_ALLOWED)