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
from django.contrib.auth import update_session_auth_hash

from rest_framework.views import APIView
<<<<<<< HEAD
=======
from django.contrib.auth import update_session_auth_hash

from rest_framework.views import APIView
>>>>>>> 3db01b4c4d74bec719c1b9a19af89a763a215890
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
                # name=user.first_name + " " + user.last_name,  # Or however you want to set the name
                first_name=user.first_name ,
                last_name=user.last_name ,
<<<<<<< HEAD
=======
                # name=user.first_name + " " + user.last_name,  # Or however you want to set the name
                first_name=user.first_name ,
                last_name=user.last_name ,
>>>>>>> 3db01b4c4d74bec719c1b9a19af89a763a215890
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
    
    #API dùng query parameter-----------------------------------------
<<<<<<< HEAD
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes

@api_view(['GET','POST', 'PUT','PATCH', 'DELETE'])
@permission_classes([AllowAny]) 
=======


@api_view(['GET','POST', 'PUT','PATCH', 'DELETE'])
>>>>>>> 3db01b4c4d74bec719c1b9a19af89a763a215890
def product2_list(request):
    product_id = request.GET.get('id')  # Lấy id từ query parameters
    show_quantity = request.GET.get('show_quantity', False)  # Kiểm tra có yêu cầu hiển thị quantity hay không
    if request.method == 'GET':
        if product_id:
            try:
                product = Product.objects.get(id=product_id)  # Tìm sản phẩm theo id
                serializer = ProductSerializer(product, context={'request': request, 'show_quantity': show_quantity})
                return Response(serializer.data)
            except Product.DoesNotExist:
                return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            products = Product.objects.all()  # Nếu không có id, lấy tất cả sản phẩm
            serializer = ProductSerializer(products, many=True, context={'request': request, 'show_quantity': show_quantity})
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
<<<<<<< HEAD
     # Các phương thức PUT, PATCH, DELETE tương tự cần IsAuthenticated
    elif request.method in ['PUT', 'PATCH', 'DELETE']:
        permission_classes([IsAuthenticated])  # Chỉ cho phép người dùng đã xác thực thực hiện các hành động này
        # Xử lý các hành động PUT, PATCH, DELETE...
=======
>>>>>>> 3db01b4c4d74bec719c1b9a19af89a763a215890

#------------------------------------------------------------------------------------
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
    
#API dùng query parameter-----------------------------------------
@api_view(['GET','POST', 'PUT','PATCH', 'DELETE'])
def producttype2_list(request):
    producttype_id = request.GET.get('id')  # Lấy id từ query parameters
    if request.method == 'GET':
        if producttype_id:
            try:
                producttype = ProductType.objects.get(id=producttype_id)  # Tìm sản phẩm theo id
                serializer = ProductTypeSerializer(producttype)
                return Response(serializer.data)
            except Product.DoesNotExist:
                return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            producttypes = ProductType.objects.all()  # Nếu không có id, lấy tất cả sản phẩm
            serializer = ProductTypeSerializer(producttypes, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            producttype = ProductType.objects.get(id=producttype_id)
        except ProductType.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductTypeSerializer(producttype, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        try:
            producttype = ProductType.objects.get(id=producttype_id)
        except ProductType.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductTypeSerializer(producttype, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            producttype = ProductType.objects.get(id=producttype_id)
            producttype.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProductType.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
#------------------------------------------------------------------------------------
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
@api_view(['GET', 'PUT', 'DELETE'])
def customer_detail(request, pk):
    try:
        customer = Customer.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            #serializer.save()
            updated_customer  = serializer.save()
            # user = User.objects.create(
            #     #username=customer.email,  # Sử dụng email làm username
            #     email=customer.email,
            #     first_name=customer.first_name,
            #     last_name=customer.last_name
            # )
            # user.save()
            user = customer.user  # Truy cập đối tượng User đã liên kết với Customer
            user.first_name = updated_customer.first_name
            user.last_name = updated_customer.last_name
            user.email = updated_customer.email
            user.save()  # Lưu lại thông tin User đã được cập nhật


            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        # customer.delete()
        if customer.user:
              customer.user.delete() 
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#API dùng query parameter-----------------------------------------
@api_view(['GET', 'PUT','PATCH', 'DELETE'])
def customer2_list(request):
    customer_id = request.GET.get('id')  # Lấy id từ query parameters

    if request.method == 'GET':
        if customer_id:
            try:
                customer = Customer.objects.get(id=customer_id)  # Tìm sản phẩm theo id
                serializer = CustomerSerializer(customer)
                return Response(serializer.data)
            except Customer.DoesNotExist:
                return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            customer = Customer.objects.all()  # Nếu không có id, lấy tất cả sản phẩm
            serializer = CustomerSerializer(customer, many=True)
            return Response(serializer.data)

    # if request.method == 'GET':
    #     serializer = CustomerSerializer(customer)
        # return Response(serializer.data)
    elif request.method == 'PUT':
        customer = Customer.objects.get(id=customer_id)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            updated_customer = serializer.save()
            
            # Cập nhật thông tin User đã liên kết
            user = customer.user
            user.first_name = updated_customer.first_name
            user.last_name = updated_customer.last_name
            user.email = updated_customer.email
            user.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        customer = Customer.objects.get(id=customer_id)
        # PATCH chỉ cập nhật những trường có dữ liệu trong request
        serializer = CustomerSerializer(customer, data=request.data, partial=True)  # partial=True để cho phép cập nhật một phần dữ liệu
        if serializer.is_valid():
            updated_customer = serializer.save()

            # Cập nhật thông tin User đã liên kết, tương tự như PUT
            user = customer.user
            if updated_customer.first_name:
                user.first_name = updated_customer.first_name
            if updated_customer.last_name:
                user.last_name = updated_customer.last_name
            if updated_customer.email:
                user.email = updated_customer.email
            user.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        customer = Customer.objects.get(id=customer_id)
        if customer_id.user:
            customer_id.user.delete()
        customer_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#------------------------------------------------------------------------------------
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


#API dùng query parameter-----------------------------------------
@api_view(['GET','POST', 'PUT','PATCH', 'DELETE'])
def supplier2_list(request):
    supplier_id = request.GET.get('id')  # Lấy id từ query parameters
    if request.method == 'GET':
        if supplier_id:
            try:
                supplier = Supplier.objects.get(id=supplier_id)  # Tìm sản phẩm theo id
                serializer = SupplierSerializer(supplier)
                return Response(serializer.data)
            except Supplier.DoesNotExist:
                return Response({"detail": "Supplier not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            suppliers = Supplier.objects.all()  # Nếu không có id, lấy tất cả sản phẩm
            serializer = SupplierSerializer(suppliers, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            supplier = Supplier.objects.get(id=supplier_id)
        except Supplier.DoesNotExist:
            return Response({"detail": "Supplier not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SupplierSerializer(supplier, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        try:
            supplier = Supplier.objects.get(id=supplier_id)
        except Supplier.DoesNotExist:
            return Response({"detail": "Supplier not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SupplierSerializer(supplier, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            supplier = Supplier.objects.get(id=supplier_id)
            supplier.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Supplier.DoesNotExist:
            return Response({"detail": "Supplier not found."}, status=status.HTTP_404_NOT_FOUND)
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#Receipt 
@api_view(['GET', 'POST'])
#@parser_classes([MultiPartParser, FormParser])
def receipt_list(request):
    if request.method == "GET":
        receiptdetail = ReceiptDetail.objects.all()
        serializer = ReceiptDetailSerializer(receiptdetail, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ReceiptDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def receipt_detail(request, pk):
    try:
        receiptdetail = ReceiptDetail.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ReceiptSerializer(receiptdetail)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ReceiptSerializer(receiptdetail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        receiptdetail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
        #API dùng query parameter-----------------------------------------
@api_view(['GET','POST', 'PUT','PATCH', 'DELETE'])
def receipt2_list(request):
    receipt_id = request.GET.get('id')  # Lấy id từ query parameters
    if request.method == 'GET':
        if receipt_id:
            try:
                receipt = Receipt.objects.get(id=receipt_id)  # Tìm sản phẩm theo id
                serializer = ReceiptSerializer(receipt)
                return Response(serializer.data)
            except Receipt.DoesNotExist:
                return Response({"detail": "Receipt not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            receipts = Receipt.objects.all()  # Nếu không có id, lấy tất cả sản phẩm
            serializer = ReceiptSerializer(receipts, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ReceiptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            receipt = Receipt.objects.get(id=receipt_id)
        except Receipt.DoesNotExist:
            return Response({"detail": "Receipt not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ReceiptSerializer(receipt, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        try:
            receipt = Receipt.objects.get(id=receipt_id)
        except Receipt.DoesNotExist:
            return Response({"detail": "Receipt not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ReceiptSerializer(receipt, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            receipt = Receipt.objects.get(id=receipt_id)
            receipt.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Receipt.DoesNotExist:
            return Response({"detail": "Receipt not found."}, status=status.HTTP_404_NOT_FOUND)
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#ReceiptDetail
@api_view(['GET', 'POST'])
#@parser_classes([MultiPartParser, FormParser])
def receiptdetail_list(request):
    if request.method == "GET":
        receipt = Receipt.objects.all()
        serializer = ReceiptSerializer(receipt, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ReceiptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def receiptdetail_detail(request, pk):
    try:
        receipt = Receipt.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ReceiptSerializer(receipt)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ReceiptSerializer(receipt, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        receipt.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#API dùng query parameter-----------------------------------------
@api_view(['GET','POST', 'PUT','PATCH', 'DELETE'])
def receiptdetail2_list(request):
    receiptdetail_id = request.GET.get('id')  # Lấy id từ query parameters
    if request.method == 'GET':
        if receiptdetail_id:
            try:
                receiptdetail = ReceiptDetail.objects.get(id=receiptdetail_id)  # Tìm sản phẩm theo id
                serializer = ReceiptDetailSerializer(receiptdetail)
                return Response(serializer.data)
            except ReceiptDetail.DoesNotExist:
                return Response({"detail": "ReceiptDetail not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            receiptdetails = ReceiptDetail.objects.all()  # Nếu không có id, lấy tất cả sản phẩm
            serializer = ReceiptDetailSerializer(receiptdetails, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ReceiptDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            receiptdetail = ReceiptDetail.objects.get(id=receiptdetail_id) 
        except ReceiptDetail.DoesNotExist:
            return Response({"detail": "ReceiptDetail not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ReceiptDetailSerializer(receiptdetail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        try:
            receiptdetail = ReceiptDetail.objects.get(id=receiptdetail_id) 
        except Receipt.DoesNotExist:
            return Response({"detail": "Receipt not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ReceiptDetailSerializer(receiptdetail, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            receiptdetail = ReceiptDetail.objects.get(id=receiptdetail_id) 
            receiptdetail.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ReceiptDetail.DoesNotExist:
            return Response({"detail": "ReceiptDetail not found."}, status=status.HTTP_404_NOT_FOUND)
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#Order
@api_view(['GET', 'POST'])
#@parser_classes([MultiPartParser, FormParser])
def order_list(request):
    if request.method == "GET":
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#API dùng query parameter-----------------------------------------
@api_view(['GET','POST', 'PUT','PATCH', 'DELETE'])
def order2_list(request):
    order_id = request.GET.get('id')  # Lấy id từ query parameters
    if request.method == 'GET':
        if order_id:
            try:
                order = Order.objects.get(id=order_id)  # Tìm sản phẩm theo id
                serializer = OrderSerializer(order)
                return Response(serializer.data)
            except Order.DoesNotExist:
                return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            orders = Order.objects.all()  # Nếu không có id, lấy tất cả sản phẩm
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            order = Order.objects.get(id=order_id)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#OrderItem
@api_view(['GET', 'POST'])
#@parser_classes([MultiPartParser, FormParser])
def orderitem_list(request):
    if request.method == "GET":
        orderitem = OrderItem.objects.all()
        serializer = OrderItemSerializer(orderitem, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def orderitem_detail(request, pk):
    try:
        orderitem = OrderItem.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = OrderItemSerializer(orderitem)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = OrderItemSerializer(orderitem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        orderitem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#API dùng query parameter-----------------------------------------
@api_view(['GET','POST', 'PUT','PATCH', 'DELETE'])
def orderitem2_list(request):
    orderitem_id = request.GET.get('id')  # Lấy id từ query parameters
    if request.method == 'GET':
        if orderitem_id:
            try:
                orderitem = OrderItem.objects.get(id=orderitem_id)  # Tìm sản phẩm theo id
                serializer = OrderItemSerializer(orderitem)
                return Response(serializer.data)
            except OrderItem.DoesNotExist:
                return Response({"detail": "OrderItem not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            orderitems = OrderItem.objects.all()  # Nếu không có id, lấy tất cả sản phẩm
            serializer = OrderItemSerializer(orderitems, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try:
            orderitem = OrderItem.objects.get(id=orderitem_id) 
        except OrderItem.DoesNotExist:
            return Response({"detail": "OrderItem not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderItemSerializer(orderitem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        try:
            orderitem = OrderItem.objects.get(id=orderitem_id) 
        except OrderItem.DoesNotExist:
            return Response({"detail": "OrderItem not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderItemSerializer(orderitem, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            orderitem = OrderItem.objects.get(id=orderitem_id) 
            orderitem.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except OrderItem.DoesNotExist:
            return Response({"detail": "OrderItem not found."}, status=status.HTTP_404_NOT_FOUND)
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#Register: false
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
                #name=user.first_name + " " + user.last_name,
                first_name=user.first_name ,
                last_name=user.last_name ,
<<<<<<< HEAD
=======
                #name=user.first_name + " " + user.last_name,
                first_name=user.first_name ,
                last_name=user.last_name ,
>>>>>>> 3db01b4c4d74bec719c1b9a19af89a763a215890
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

#-------------------------------------------------------------------------------
#Register_1: false
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User registered successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Registration failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
#---------------------------------------------------------------------------
#Register_2: false (có sử dụng 1 phần cho đoạn chạy được)
class RegisterAPI(APIView):
    def post(self, request):
        # Tạo form từ dữ liệu POST
        form = CreateUserForm(request.data)
        
        if form.is_valid():
            # Lưu user
            user = form.save()
            user.is_staff = True  # Set is_staff to True
            user.save()

            # Tạo customer
            Customer.objects.create(
                user=user,
                #name=user.first_name + " " + user.last_name,
                first_name=user.first_name ,
                last_name=user.last_name ,
                email=user.email
            )

            # Trả về phản hồi thành công
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

        # Nếu form không hợp lệ
        return Response({
            'errors': form.errors
        }, status=status.HTTP_400_BAD_REQUEST)
#---------------------------------------------------------------------------------
# users/views.py
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer

# API cho việc lấy danh sách và chi tiết người dùng
class UserList(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserDetail(APIView):
    def get(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # def put(self, request, pk, format=None):
    #     try:
    #         user = User.objects.get(pk=pk)
    #     except User.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

    #     serializer = UserSerializer(user, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            customer = Customer.objects.get(user=user)
            customer.delete()  # Xóa Customer liên kết với User
        except Customer.DoesNotExist:
            pass  # Nếu không có Customer, thì không cần làm gì cả
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#---------------------------------------------------------------
#--------------------------------------------------------------------
#--------------------------------------------------------------------
#Code chuẩn 
# Tạo API cho việc tạo người dùng
class UserCreate(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        form = CreateUserForm(request.data)
        if serializer.is_valid():
            
            user = serializer.save()
            user.is_staff = True 
            user.save()
            # form.is_staff = True 
            # CustomerSerializer.objects.create(
            #     user=serializer.username,
            #     name=serializer.first_name + " " + serializer.last_name,
            #     email=serializer.email
            # )
            Customer.objects.create(
                user=user,  # Use the saved user object
                # name=user.last_name+ " " + user.first_name ,  # Concatenate first and last name
                first_name=user.first_name ,
                last_name=user.last_name ,
                email=user.email
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#------------------------------------------------------------------
#Có thể dùng
class ChangePassword(APIView):
    def put(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({"detail": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)  # Mã hóa mật khẩu mới
        user.save()

        # Đảm bảo rằng phiên người dùng không bị hỏng sau khi thay đổi mật khẩu
        update_session_auth_hash(request, user)

        return Response({"detail": "Password updated successfully"})
#---------------------------------------------------------------------
#update thông tin user (Chưa dùng)
class UserUpdate(APIView):
    def put(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer_update(user, data=request.data, partial=True)  # partial=True để chỉ cập nhật các trường có trong request
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#---------------------------------------------------------------------    
#Tạo thông tin user có phone của customer (Chưa dùng)
class CreateUserWithPhone(APIView):
    def post(self, request):
        # Nhận dữ liệu từ client
        #serializer = UserSerializer_customer(data=request.data)
        serializer = CustomerSerializer_user(data=request.data)
        
        if serializer.is_valid():
            # Lưu người dùng và thông tin customer
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#--------------------------------------------------------------------
#--------------------------------------------------------------------
#--------------------------------------------------------------------
#Code cập nhật dữ liệu users
class UpdateUserAPIView(APIView):
    def put(self, request, pk):
        try:
            # Lấy đối tượng User từ ID (pk)
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Cập nhật dữ liệu User
        serializer = UserSerializer(user, data=request.data, partial=True)

        customer = Customer.objects.filter(user=user).first()

# Nếu Customer không tồn tại, tạo mới. Nếu có rồi thì cập nhật.
        if customer != 0:
            # Cập nhật thông tin
            #customer.name = user.last_name + " " + user.first_name
            customer.last_name=user.last_name
            customer.first_name=user.first_name
            customer.email = user.email
            customer.save()  # Lưu các thay đổi
        
        if serializer.is_valid():
            # Lưu thay đổi vào cơ sở dữ liệu
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#------------------------------------------------------
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

class LoginAPIView(APIView):
    permission_classes = [AllowAny]  # Cho phép tất cả mọi người truy cập API đăng nhập

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Kiểm tra thông tin đăng nhập
        user = User.objects.filter(username=username).first()
        if user is None or not user.check_password(password):
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Lấy token hoặc tạo token mới cho user
        token, created = Token.objects.get_or_create(user=user)

        # Trả về thông tin người dùng và token
        user_data = UserSerializer(user).data
        return Response({
            "token": token.key,
            "user": user_data
        })
#---------------------------------------------------------------------------
from rest_framework.permissions import IsAuthenticated
import logging
logger = logging.getLogger(__name__)

class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Chỉ cho phép người dùng đã đăng nhập truy cập API này

    def get(self, request, *args, **kwargs):
        # Lấy user hiện tại từ request
        user = request.user
        logger.debug(f"User: {user.username} is requesting cart.")
        # Tìm tất cả các đơn hàng chưa hoàn thành (complete=False) của người dùng
        #orders = Order.objects.filter(customer=user, complete=False)
        orders = Order.objects.filter(customer=user)        
        if not orders.exists():
            return Response({"detail": "No active order found."}, status=status.HTTP_404_NOT_FOUND)

        # Lấy tất cả các sản phẩm trong OrderItem của các đơn hàng chưa hoàn thành
        order_items = OrderItem.objects.filter(order__in=orders)
        logger.debug(f"Found {order_items.count()} order items.")

        # Nếu không có sản phẩm nào trong giỏ hàng
        if not order_items.exists():
            return Response({"detail": "Your cart is empty."}, status=status.HTTP_200_OK)
        
        # Lấy thông tin sản phẩm từ OrderItem và trả về
        products = [item.product for item in order_items]
        serializer = ProductSerializer(products, many=True)
        logger.debug(f"Returning {len(serializer.data)} products.")
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
from rest_framework_simplejwt.tokens import RefreshToken
class LoginAPIView_1(APIView):
    permission_classes = [AllowAny]  # Cho phép tất cả mọi người truy cập API đăng nhập

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Kiểm tra thông tin đăng nhập
        user = User.objects.filter(username=username).first()
        if user is None or not user.check_password(password):
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Lấy token hoặc tạo token mới cho user
        #token, created = Token.objects.get_or_create(user=user)

            # Tạo token JWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Trả về thông tin người dùng và token
        user_data = UserSerializer(user).data
        return Response({
            "access_token": access_token,
            "user": user_data
        })
#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
#Login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class LoginView_3(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            return Response({
                'access': str(access_token),
                'refresh': str(refresh),
            })
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Order
from .serializers import OrderSerializer
#Sai code chỗ product
class CartView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]  # Đảm bảo người dùng phải đăng nhập
    serializer_class = OrderSerializer

    def get_object(self):
        user = self.request.user  # Lấy user đã đăng nhập
        
        if not user.is_authenticated:  # Kiểm tra nếu người dùng chưa đăng nhập
            raise ValueError("User is not authenticated")
        try:
            # Lấy Customer instance từ User
            customer = Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            raise ValueError("Customer instance not found for the user.")

        # Tạo hoặc lấy Order của khách hàng (giỏ hàng chưa hoàn tất)
        # order, created = Order.objects.get_or_create(
        #     customer=customer,
        #     complete=False  # Giỏ hàng chưa hoàn tất
        # )
        # return order

           # Lấy tất cả các OrderItem thuộc về đơn hàng chưa hoàn tất của người dùng
        # order_items = OrderItem.objects.filter(order__customer=customer, order__complete=False)
        # return order_items


        # Lấy tất cả các OrderItem thuộc đơn hàng của khách hàng
        # (bao gồm cả các đơn hàng đã hoàn tất hoặc chưa hoàn tất)
        order_items = OrderItem.objects.filter(
            order__customer=customer  # Lọc theo khách hàng
        )
        
        # Lấy danh sách các đối tượng Product từ các OrderItem
        # Sử dụng distinct() để đảm bảo không bị trùng lặp sản phẩm nếu cùng một sản phẩm được đặt nhiều lần
        products = Product.objects.filter(
            id__in=[order_item.product.id for order_item in order_items]
        ).distinct()

        return products
#------------------------------------------------------------------------
from rest_framework_simplejwt.authentication import JWTAuthentication
 # Sử dụng JWTAuthentication thay vì TokenAuthentication
class CartView_2(generics.ListAPIView):  # Chúng ta sử dụng ListAPIView vì chúng ta muốn trả về danh sách sản phẩm
    permission_classes = [IsAuthenticated]  # Đảm bảo người dùng phải đăng nhập
    serializer_class = ProductSerializer  # Sử dụng serializer cho Product
    # authentication_classes = [TokenAuthentication]
    authentication_classes = [JWTAuthentication]  # Sử dụng JWTAuthentication thay vì TokenAuthentication

    def get_queryset(self):
        user = self.request.user  # Lấy user đã đăng nhập
        
        if not user.is_authenticated:  # Kiểm tra nếu người dùng chưa đăng nhập
            raise ValueError("User is not authenticated")

        try:
            # Lấy Customer instance từ User
            customer = Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            raise ValueError("Customer instance not found for the user.")

        # Lấy các OrderItem từ các đơn hàng chưa hoàn tất (complete=False)
        order_items = OrderItem.objects.filter(order__customer=customer, order__complete=False)

        # Trả về danh sách các sản phẩm từ các OrderItem
        products = Product.objects.filter(id__in=[item.product.id for item in order_items])

        return products
    
    def get_serializer_context(self):
        # Thêm show_quantity vào context chỉ khi gọi CartView
        context = super().get_serializer_context()
        context['show_quantity'] = True
        return context
    
#-----------------------------------------------------------------------------
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'detail': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Xác thực người dùng
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Đăng nhập người dùng và tạo session
            return Response({'detail': 'Login successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
<<<<<<< HEAD
        
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
# views.py
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def create_order(request):
    if request.user.is_authenticated:
        order = Order.objects.create(customer=request.user)
        return Response({'id': order.id}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
def add_to_cart(request):
    if request.user.is_authenticated:
        order_id = request.data.get('order')
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)

        try:
            order = Order.objects.get(id=order_id, customer=request.user)
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
            return Response({'message': 'Product added to cart'}, status=status.HTTP_201_CREATED)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_cart(request):
    if request.user.is_authenticated:
        order = Order.objects.filter(customer=request.user, complete=False).first()
        if order:
            return Response({'id': order.id, 'items': order.items.all()})
        return Response({'error': 'No active cart'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
@api_view(['POST'])
def add_to_cart_1(request):
    if not request.user.is_authenticated:
        return Response({"detail": "Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng."}, status=status.HTTP_401_UNAUTHORIZED)

    user = request.user  # Lấy đối tượng User
    
    # Lấy đối tượng Customer tương ứng với User (Giả sử Customer có quan hệ với User)
    try:
        customer = user.customer  # Nếu User có liên kết với Customer
    except Customer.DoesNotExist:
        return Response({"detail": "Không tìm thấy thông tin khách hàng."}, status=status.HTTP_404_NOT_FOUND)

    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)

    if not product_id:
        return Response({"detail": "Không tìm thấy thông tin sản phẩm."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"detail": "Sản phẩm không tồn tại."}, status=status.HTTP_404_NOT_FOUND)

    # Kiểm tra giỏ hàng của người dùng
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    # Thêm sản phẩm vào giỏ hàng
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if not created:
        # Cập nhật số lượng nếu sản phẩm đã có trong giỏ hàng
        order_item.quantity += quantity
        order_item.save()
    else:
        # Tạo mới sản phẩm trong giỏ hàng
        order_item.quantity = quantity
        order_item.save()

    return Response({"detail": "Sản phẩm đã được thêm vào giỏ hàng."}, status=status.HTTP_200_OK)
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import OrderItem
from .serializers import OrderItemSerializer

@api_view(['PATCH'])
def update_order_item(request, order_id, product_id):
    try:
        order_item = OrderItem.objects.get(order_id=order_id, product_id=product_id)
    except OrderItem.DoesNotExist:
        return Response({'error': 'OrderItem not found'}, status=status.HTTP_404_NOT_FOUND)

    quantity = request.data.get('quantity')
    if quantity is not None and quantity > 0:
        order_item.quantity = quantity
        order_item.save()
        return Response(OrderItemSerializer(order_item).data)
    else:
        return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
@api_view(['DELETE'])
def delete_order_item(request, order_id, product_id):
    try:
        order_item = OrderItem.objects.get(order_id=order_id, product_id=product_id)
    except OrderItem.DoesNotExist:
        return Response({'error': 'OrderItem not found'}, status=status.HTTP_404_NOT_FOUND)

    order_item.delete()
    return Response({'message': 'Product removed from cart'}, status=status.HTTP_204_NO_CONTENT)
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Order, OrderItem, Customer
from .serializers import OrderSerializer  # Giả sử bạn có serializer cho Order

class Get_order(generics.ListAPIView):  
    permission_classes = [IsAuthenticated]  # Đảm bảo người dùng phải đăng nhập
    serializer_class = OrderSerializer  # Sử dụng serializer cho Order
    authentication_classes = [JWTAuthentication]  # Sử dụng JWTAuthentication thay vì TokenAuthentication

    def get_queryset(self):
        user = self.request.user  # Lấy user đã đăng nhập
        
        if not user.is_authenticated:  # Kiểm tra nếu người dùng chưa đăng nhập
            raise ValueError("User is not authenticated")

        try:
            # Lấy Customer instance từ User
            customer = Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            raise ValueError("Customer instance not found for the user.")

        # Lấy các Order của Customer với điều kiện là chưa hoàn tất (complete=False)
        orders = Order.objects.filter(customer=customer, complete=False)
        print(orders)
        return orders
    
    #---------------------------------------------------------------------------
    
class get_orderitem(generics.ListAPIView):  # Chúng ta sử dụng ListAPIView vì chúng ta muốn trả về danh sách sản phẩm
    permission_classes = [IsAuthenticated]  # Đảm bảo người dùng phải đăng nhập
    serializer_class = OrderItemSerializer  # Sử dụng serializer cho Product
    # authentication_classes = [TokenAuthentication]
    authentication_classes = [JWTAuthentication]  # Sử dụng JWTAuthentication thay vì TokenAuthentication

    def get_queryset(self):
        user = self.request.user  # Lấy user đã đăng nhập
        
        if not user.is_authenticated:  # Kiểm tra nếu người dùng chưa đăng nhập
            raise ValueError("User is not authenticated")

        try:
            # Lấy Customer instance từ User
            customer = Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            raise ValueError("Customer instance not found for the user.")

        # Lấy các OrderItem từ các đơn hàng chưa hoàn tất (complete=False)
        order_items = OrderItem.objects.filter(order__customer=customer, order__complete=False)

        # Trả về danh sách các sản phẩm từ các OrderItem
        products = Product.objects.filter(id__in=[item.product.id for item in order_items])

        return order_items
#--------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Product
from .serializers import ProductSerializer
class ProductSearchView(APIView):
    def get(self, request):
        search_query = request.GET.get('search', '')
        if search_query:
            products = Product.objects.filter(
                Q(name__icontains=search_query)  # Tìm kiếm không phân biệt hoa thường
            )
        else:
            products = Product.objects.all()  # Nếu không có từ khóa tìm kiếm thì lấy tất cả sản phẩm

        # Sử dụng Serializer để trả về dữ liệu
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def product_search(request):
    search = request.GET.get('search', '')
    if search:
        products = Product.objects.filter(name__icontains=search)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    return Response([])
=======
>>>>>>> 3db01b4c4d74bec719c1b9a19af89a763a215890

