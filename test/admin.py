from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(ProductType)
admin.site.register(Receipt)
#admin.site.register(ReceiptDetail)
admin.site.register(Supplier)
@admin.register(ReceiptDetail)
class ReceiptDetailAdmin(admin.ModelAdmin):
    list_display = ('receipt', 'product', 'quantity', 'unit_price', 'subtotal')  # Hiển thị các trường
    readonly_fields = ('subtotal',)  # Đặt subtotal chỉ đọc

    def save_model(self, request, obj, form, change):
        # Đảm bảo subtotal được tính trước khi lưu
        obj.subtotal = obj.quantity * obj.unit_price
        super().save_model(request, obj, form, change)