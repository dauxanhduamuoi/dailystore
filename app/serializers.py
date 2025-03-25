from rest_framework import serializers
from .models import *  # Thay Product bằng model của bạn

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'  # Chọn tất cả các trường trong model

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        #fields = '__all__'  # Chọn tất cả các trường trong model
        fields = '__all__'  # Chọn tất cả các trường trong model

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        #fields = '__all__'  # Chọn tất cả các trường trong model
        fields = '__all__'  # Chọn tất cả các trường trong model

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        #fields = '__all__'  # Chọn tất cả các trường trong model
        fields = '__all__'  # Chọn tất cả các trường trong model

class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        #fields = '__all__'  # Chọn tất cả các trường trong model
        fields = '__all__'  # Chọn tất cả các trường trong model

class ReceiptDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptDetail
        #fields = '__all__'  # Chọn tất cả các trường trong model
        fields = '__all__'  # Chọn tất cả các trường trong model
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'  # Chọn tất cả các trường trong model
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'  # Chọn tất cả các trường trong model




# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'first_name', 'last_name']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password'],
#             first_name=validated_data.get('first_name', ''),
#             last_name=validated_data.get('last_name', ''),
#             is_staff=True
#         )
        
#         Customer.objects.create(
#             user=user,
#             name=f"{user.first_name} {user.last_name}",
#             email=user.email
#         )
#         return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password','first_name', 'last_name', 'email', 'date_joined']
    def create(self, validated_data):
        # Lấy mật khẩu và mã hóa nó
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)  # Mã hóa mật khẩu
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)  # Mã hóa mật khẩu
            user.save()
        return user

#cập nhật full user
class UserSerializer_update(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password','first_name', 'last_name', 'email', 'date_joined','phone']
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)  # Lấy mật khẩu (nếu có)
        # Cập nhật thông tin người dùng (như username, email, v.v.)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)  # Nếu có mật khẩu mới, mã hóa và lưu
        instance.save()
        return instance
#-----------------------------------------------------------------------
#Bị lỗi
class UserSerializer_customer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Tạo người dùng mới và mã hóa mật khẩu
        user = User.objects.create_user(**validated_data)
        return user

# Serializer cho Customer (bao gồm thông tin phone)
class CustomerSerializer_user(serializers.ModelSerializer):
    user = UserSerializer_customer()  # Kết nối User với Customer

    class Meta:
        model = Customer
        fields = ['user', 'phone']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')  # Lấy dữ liệu user
        user = User.objects.create_user(**user_data)  # Tạo người dùng mới
        customer = Customer.objects.create(user=user, **validated_data)  # Tạo customer
        return customer
    


#------------------------------------------------
from django.contrib.auth.hashers import make_password
class UserSerializer_update_2(serializers.ModelSerializer):
    # Mật khẩu sẽ được mã hóa lại khi có sự thay đổi
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def update(self, instance, validated_data):
        # Nếu có mật khẩu mới, cần mã hóa lại mật khẩu
        password = validated_data.get('password', None)
        if password:
            instance.password = make_password(password)

        # Cập nhật các trường còn lại
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        # Lưu lại thông tin sau khi cập nhật
        instance.save()
        return instance