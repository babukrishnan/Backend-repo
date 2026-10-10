from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order, Product, Notification

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_order_status(request, id):
    with transaction.atomic():
        try:
            order = Order.objects.select_for_update().get(pk=id)
        except Order.DoesNotExist:
            return Response({'error':'Order not found'},status=404)
        action = request.data.get('status')
        allowed = []
        if order.status == 'pending':
            allowed = ['accepted','rejected'] if request.user.pk == order.seller_id else ['cancelled'] if request.user.pk == order.buyer_id else []
        elif order.status == 'accepted' and request.user.pk == order.seller_id:
            allowed = ['completed']
        if action not in allowed:
            return Response({'error':'Invalid transition'},status=403)
        if action in ('rejected','cancelled'):
            product = Product.objects.select_for_update().get(pk=order.product_id)
            product.quantity += order.quantity
            product.save(update_fields=['quantity'])
        order.status = action
        order.save(update_fields=['status'])
        recipient = order.buyer if request.user.pk == order.seller_id else order.seller
        Notification.objects.create(user=recipient,order=order,message=f'Order {order.pk}: {action}')
        return Response({'id':order.pk,'status':order.status})
