from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=100)
    shop = models.CharField(max_length=200)
    description = models.TextField()
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name