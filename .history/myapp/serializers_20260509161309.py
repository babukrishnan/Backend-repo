from rest_framework import serializers
from .productModel import Product
from .models import FarmerProfile

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class FarmerProfileSerializer( serializers.ModelSerializer):

    class Meta:

        model = FarmerProfile

        fields = '__all__'