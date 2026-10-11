from rest_framework import serializers
from .productModel import Product
from .profileModel import FarmerProfile

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['farmer','created_at']
    def validate_price(self,value):
        if value <= 0:
            raise serializers.ValidationError('Price must be positive')
        return value
    def validate_quantity(self,value):
        if value < 0:
            raise serializers.ValidationError('Quantity cannot be negative')
        return value

class FarmerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProfile
        fields = '__all__'
        read_only_fields = ['user','is_completed']
