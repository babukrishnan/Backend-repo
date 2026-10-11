from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product, Order, Notification

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def orders(request):
    if request.method == 'GET':
        field = request.query_params.get('as','buyer')
        if field not in ('buyer','seller'):
            return Response({'error':'Invalid role'},status=400)
        qs = Order.objects.filter(**{field:request.user}).order_by('-created_at')[:100]
        return Response(list(qs.values()))
    try:
        pid = int(request.data.get('product_id',0))
        qty = int(request.data.get('quantity',0))
    except (TypeError,ValueError):
        return Response({'error':'Invalid input'},status=400)
    phone = str(request.data.get('contact_phone','')).strip()
    address = str(request.data.get('delivery_address','')).strip()
    if qty < 1 or not phone or len(address)<5:
        return Response({'error':'Invalid input'},status=400)
    with transaction.atomic():
        try:
            product = Product.objects.select_for_update().get(pk=pid)
        except Product.DoesNotExist:
            return Response({'error':'Not found'},status=404)
        if product.farmer_id == request.user.pk or product.quantity < qty:
            return Response({'error':'Unavailable'},status=400)
        order = Order.objects.create(buyer=request.user,seller=product.farmer,product=product,
          product_name=product.name,quantity=qty,unit_price=product.price,
          total_amount=qty*product.price,contact_phone=phone,delivery_address=address)
        product.quantity -= qty
        product.save(update_fields=['quantity'])
        Notification.objects.create(user=product.farmer,order=order,message='New order')
    return Response({'id':order.id,'status':order.status},status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notifications(request):
    qs = Notification.objects.filter(user=request.user).order_by('-created_at')[:100]
    return Response(list(qs.values()))
