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
