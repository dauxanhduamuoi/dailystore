from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#Test
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.
# Change forms register django
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']
#Class thử nghiệm
# class Customer_User(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
#     address = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return self.user.username
# class CustomUser(AbstractUser):
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
#     address = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return self.username


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL,null=True,blank=False)
    #name = models.CharField(max_length=200,null=True)
    last_name = models.CharField(max_length=200,null=True)
    first_name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    # def __str__(self):
    #     return self.name
    def __str__(self):
     if self.last_name and self.first_name:
            return str(self.user.username+': ' + self.last_name +' ' + self.first_name) # Convert to string in case it's not
     elif self.user:
            return str(self.user.username)
     else:
        return "Customer without username"  # Or some other default string


# Bảng Nhà cung cấp
class Supplier(models.Model):
    name = models.CharField(max_length=200, unique=True)  # Tên nhà cung cấp, duy nhất
    phone = models.CharField(max_length=20, null=True, blank=True)  # Số điện thoại
    email = models.EmailField(null=True, blank=True)  # Email
    address = models.TextField(null=True, blank=True)  # Địa chỉ
    

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['name']  # Sắp xếp theo tên

# Bảng Phiếu nhập (cập nhật với Supplier)
class Receipt(models.Model):
    #receipt_code = models.CharField(max_length=50, unique=True)  # Mã phiếu nhập
    created_date = models.DateTimeField(default=timezone.now)    # Ngày tạo phiếu
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)  # Liên kết với Supplier
    total_amount = models.FloatField(default=0.0)                # Tổng tiền
    #created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)  # Người tạo

    # def __str__(self):
    #     #return f"Receipt {self.receipt_code}"
    #     return f"Receipt {self.id}"
    def __str__(self):
        #return f"Receipt {self.receipt_code}"
        return str(self.id)
    class Meta:
        ordering = ['-created_date']  # Sắp xếp theo ngày tạo giảm dần




class ProductType(models.Model):
    name = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(max_length=200, null=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.name)
    # def __str__(self):
    #     return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url

        except:
            url = ''
        return url



class ReceiptDetail(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='details')  # Liên kết với Receipt
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)             # Liên kết với Product
    quantity = models.PositiveIntegerField(default=1)                                      # Số lượng nhập
    unit_price = models.FloatField(default=0.0)                                            # Đơn giá tại thời điểm nhập
    subtotal = models.FloatField(editable=False, default=0.0)                                              # Thành tiền (số lượng * đơn giá)

    def save(self, *args, **kwargs):
        # Tự động tính subtotal trước khi lưu
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} - {self.quantity} - Receipt {self.receipt.id}"

    class Meta:
        verbose_name = "Receipt Detail"
        verbose_name_plural = "Receipt Details"
        unique_together = ('receipt', 'product')  # Không cho phép trùng sản phẩm trong cùng phiếu nhập

# Bảng Chi tiết phiếu nhập (giữ nguyên)
# class ReceiptDetail(models.Model):
#     #receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='details',blank=True,null=True) 
#     receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE,blank=True,null=True) # Liên kết với phiếu nhập
#     product = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True,null=True)  # Sản phẩm nhập
#     quantity = models.PositiveIntegerField(default=1)               # Số lượng
#     # unit_price = models.FloatField(default=1)                                # Đơn giá tại thời điểm nhập
#     # subtotal = models.FloatField(editable=False)                    # Thành tiền (tự động tính)

#     # def save(self, *args, **kwargs):
#     #     # Tự động tính subtotal trước khi lưu
#     #     self.subtotal = self.quantity * self.unit_price
#     #     super().save(*args, **kwargs)

#     # def __str__(self):
        
#     #     #return f"{self.product.name} - {self.quantity} units"

#     # def __str__(self):
#     #     #return f"Receipt {self.receipt_code}"
#     #     return f"Receipt {self.id}"

#     # def __str__(self):
#     #     #return f"Receipt {self.receipt_code}"
#     #     return str(self.id)
    
#     # def __str__(self):
#     #     # Nếu có id thì trả về id dưới dạng chuỗi, nếu không thì trả về thông tin mặc định
#     #     if self.id is not None:
#     #         return f"Detail {self.id}"
#     #     return "New Receipt Detail"

#     # def __str__(self):
#     #     product_name = self.product.name if self.product and self.product.name else "No Product"
#     #     receipt_id = self.receipt.id if self.receipt and self.receipt.id else "No Receipt"
#     #     return f"{product_name} - {self.quantity} units (Receipt {receipt_id})"

#     # def __str__(self):
#     #     # Trả về chuỗi đại diện cho đối tượng
#     #     product_name = self.product.name if hasattr(self.product, 'name') else str(self.product)
#     #     receipt_id = self.receipt.id if hasattr(self.receipt, 'id') else str(self.receipt)
#     #     return f"Receipt {receipt_id} - {product_name} (Qty: {self.quantity})"

#     # def __str__(self):
#     #     return f"{self.product.name or 'Unnamed Product'} - {self.quantity or 'Unnamed Product'} units"
#     def __str__(self):
#         return str(self.receipt)

    
#     # class Meta:
#     #     unique_together = ('receipt', 'product')  # Không cho phép trùng sản phẩm trong cùng phiếu nhập


# class Product(models.Model):
#     name = models.CharField(max_length=200,null=True)
#     price = models.FloatField(max_length=200,null=True)
#     digital = models.BooleanField(default=False,null=True,blank=False)
#     image = models.ImageField(null=True, blank=True)

#     def __str__(self):
#         return self.name
#     @property
#     def ImageURL(self):
#         try:
#             url = self.image.url

#         except:
#             url = ''
#         return url
    
class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    # name = models.CharField(max_length=200,null=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200, null=True )

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0, null=True, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    mobile = models.CharField(max_length=10, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address