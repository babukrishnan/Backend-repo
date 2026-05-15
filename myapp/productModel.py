from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    farmer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField(default=0)
    category = models.CharField(max_length=100, default='General')
    shop = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name