from rest_framework import serializers
from .productModel import Product
from .profileModel import FarmerProfile

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['farmer']


class FarmerProfileSerializer( serializers.ModelSerializer):

    class Meta:

        model = FarmerProfile

        fields = '__all__'