from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Product, Order

class MarketplaceFlowTests(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user(username='seller@test.local', password='safeTestPass123!')
        self.buyer = User.objects.create_user(username='buyer@test.local', password='safeTestPass123!')
        self.product = Product.objects.create(farmer=self.seller, name='Tomato', description='Fresh',
            price=Decimal('30.00'), quantity=5, category='Produce', shop='Farm',
            phone='9999999999')
        self.client = APIClient()
        self.payload = {'product_id': self.product.pk, 'quantity': 2,
                        'contact_phone': '9999999999', 'delivery_address': 'Madurai, Tamil Nadu'}

    def test_order_create_and_reject(self):
        self.client.force_authenticate(user=self.buyer)
        response = self.client.post('/api/orders/', self.payload, format='json')
        self.assertEqual(response.status_code, 201, response.data)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 3)
        order = Order.objects.get(pk=response.data['id'])
        self.assertEqual(order.total_amount, Decimal('60.00'))
        self.assertEqual(self.client.patch(f'/api/orders/{order.pk}/status/', {'status':'accepted'}, format='json').status_code, 403)
        self.client.force_authenticate(user=self.seller)
        self.assertEqual(self.client.patch(f'/api/orders/{order.pk}/status/', {'status':'rejected'}, format='json').status_code, 200)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 5)

    def test_invalid_order_and_owner_protection(self):
        self.client.force_authenticate(user=self.buyer)
        self.assertEqual(self.client.post('/api/orders/', {**self.payload, 'quantity': 100}, format='json').status_code, 400)
        self.assertEqual(self.client.delete(f'/api/products/{self.product.pk}/').status_code, 403)

    def test_authentication_required(self):
        self.assertEqual(self.client.get('/api/orders/').status_code, 401)
        self.assertEqual(self.client.get('/api/notifications/').status_code, 401)
