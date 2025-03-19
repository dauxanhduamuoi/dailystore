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

