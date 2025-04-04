#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#Product
@api_view(['GET','POST', 'PUT','PATCH', 'DELETE'])
def product2_list(request):
    product_id = request.GET.get('id')  # Lấy id từ query parameters
    product = Product.objects.get(pk=product_id)
    # Kiểm tra nếu không có id trong query parameters
    # if not product_id:
    #     return Response({"error": "ID không được cung cấp."}, status=status.HTTP_400_BAD_REQUEST)

    # try:
    #     product = Product.objects.get(pk=product_id)
    # except Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)

    # if request.method == 'GET':
    #     # Nếu có id, tìm sản phẩm với id đó
    #     if product_id:
    #         try:
    #             product = Product.objects.get(pk=product_id)
    #         except Product.DoesNotExist:
    #             return Response(status=status.HTTP_404_NOT_FOUND)
    #         serializer = ProductSerializer(product)
    #         return Response(serializer.data)
        
    #     # Nếu không có id, lấy tất cả sản phẩm
    #     products = Product.objects.all()
    #     serializer = ProductSerializer(products, many=True)  # many=True để serialize danh sách sản phẩm
    #     return Response(serializer.data)
    
    # if request.method == 'GET':
    #     if product_id != None:
    #         print(product_id)
    #         try:
    #             products = Product.objects.get(id=product_id)
    #             serializer = ProductSerializer(products)
    #             return Response(serializer.data)
    #         except Product.DoesNotExist:
    #             return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
    #     else:
    #         product = Product.objects.all()
    #         serializer = ProductSerializer(product, many=True)
    #         return Response(serializer.data)

    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)



    # if request.method == 'GET':
    #     serializer = ProductSerializer(product)
    #     return Response(serializer.data)

    # if request.method == 'GET':
    #     if product_id:
    #         try:
    #             product = Product.objects.get(id=product_id)  # Tìm sản phẩm theo id
    #             serializer = ProductSerializer(product)
    #             return Response(serializer.data)
    #         except Product.DoesNotExist:
    #             return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
    #     else:
    #         products = Product.objects.all()  # Nếu không có id, lấy tất cả sản phẩm
    #         serializer = ProductSerializer(products, many=True)
    #         return Response(serializer.data)

    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        # PATCH chỉ cập nhật những trường có dữ liệu trong request
        serializer = ProductSerializer(product, data=request.data, partial=True)  # partial=True để cho phép cập nhật một phần dữ liệu
        if serializer.is_valid():
            serializer.save()


            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#Producttype
@api_view(['GET', 'PUT','PATCH', 'DELETE'])
def producttype2_list(request):
    producttype_id = request.GET.get('id')  # Lấy id từ query parameters

    # Kiểm tra nếu không có id trong query parameters
    if not producttype_id:
        return Response({"error": "ID không được cung cấp."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        producttype = ProductType.objects.get(pk=producttype_id)
    except ProductType.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductTypeSerializer(producttype)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductTypeSerializer(producttype, data=request.data)
        if serializer.is_valid():
            serializer.save()
            

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        # PATCH chỉ cập nhật những trường có dữ liệu trong request
        serializer = ProductTypeSerializer(producttype, data=request.data, partial=True)  # partial=True để cho phép cập nhật một phần dữ liệu
        if serializer.is_valid():
            serializer.save()


            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        producttype.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#Supplier
@api_view(['GET', 'PUT','PATCH', 'DELETE'])
def supplier2_list(request):
    supplier_id = request.GET.get('id')  # Lấy id từ query parameters

    # Kiểm tra nếu không có id trong query parameters
    if not supplier_id:
        return Response({"error": "ID không được cung cấp."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        supplier = Supplier.objects.get(pk=supplier_id)
    except Supplier.DoesNotExist:
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
    elif request.method == 'PATCH':
        # PATCH chỉ cập nhật những trường có dữ liệu trong request
        serializer = SupplierSerializer(supplier, data=request.data, partial=True)  # partial=True để cho phép cập nhật một phần dữ liệu
        if serializer.is_valid():
            serializer.save()


            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        supplier.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#Receipt
@api_view(['GET', 'PUT','PATCH', 'DELETE'])
def receipt2_list(request):
    receipt_id = request.GET.get('id')  # Lấy id từ query parameters

    # Kiểm tra nếu không có id trong query parameters
    if not receipt_id:
        return Response({"error": "ID không được cung cấp."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        receipt = Receipt.objects.get(pk=receipt_id)
    except Receipt.DoesNotExist:
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
    elif request.method == 'PATCH':
        # PATCH chỉ cập nhật những trường có dữ liệu trong request
        serializer = ReceiptSerializer(receipt, data=request.data, partial=True)  # partial=True để cho phép cập nhật một phần dữ liệu
        if serializer.is_valid():
            serializer.save()


            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        receipt.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#ReceiptDetail
@api_view(['GET', 'PUT','PATCH', 'DELETE'])
def receiptdetail2_list(request):
    receiptdetail_id = request.GET.get('id')  # Lấy id từ query parameters

    # Kiểm tra nếu không có id trong query parameters
    if not receiptdetail_id:
        return Response({"error": "ID không được cung cấp."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        receiptdetail = ReceiptDetail.objects.get(pk=receiptdetail_id)
    except ReceiptDetail.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReceiptDetailSerializer(receiptdetail)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ReceiptDetailSerializer(receiptdetail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        # PATCH chỉ cập nhật những trường có dữ liệu trong request
        serializer = ReceiptDetailSerializer(receiptdetail, data=request.data, partial=True)  # partial=True để cho phép cập nhật một phần dữ liệu
        if serializer.is_valid():
            serializer.save()


            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        receiptdetail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#Order
@api_view(['GET', 'PUT','PATCH', 'DELETE'])
def order2_list(request):
    order_id = request.GET.get('id')  # Lấy id từ query parameters

    # Kiểm tra nếu không có id trong query parameters
    if not order_id:
        return Response({"error": "ID không được cung cấp."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
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
    elif request.method == 'PATCH':
        # PATCH chỉ cập nhật những trường có dữ liệu trong request
        serializer = OrderSerializer(order, data=request.data, partial=True)  # partial=True để cho phép cập nhật một phần dữ liệu
        if serializer.is_valid():
            serializer.save()


            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#OrderItem
@api_view(['GET', 'PUT','PATCH', 'DELETE'])
def orderitem2_list(request):
    orderitem_id = request.GET.get('id')  # Lấy id từ query parameters

    # Kiểm tra nếu không có id trong query parameters
    if not orderitem_id:
        return Response({"error": "ID không được cung cấp."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        orderitem = OrderItem.objects.get(pk=orderitem_id)
    except OrderItem.DoesNotExist:
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
    elif request.method == 'PATCH':
        # PATCH chỉ cập nhật những trường có dữ liệu trong request
        serializer = OrderItemSerializer(orderitem, data=request.data, partial=True)  # partial=True để cho phép cập nhật một phần dữ liệu
        if serializer.is_valid():
            serializer.save()


            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        orderitem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)