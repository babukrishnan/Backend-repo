from rest_framework import serializers
from .productModel import Product

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'