from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .productModel import Product
from .serializers import ProductSerializer


@api_view(['GET', 'POST'])
def get_products(request):

    # GET PRODUCTS
    # =========================
    if request.method == 'GET':

        products = Product.objects.all().order_by('-created_at')

        serializer = ProductSerializer(
            products,
            many=True
        )

        return Response(serializer.data)

    # CREATE PRODUCT
    # =========================
    elif request.method == 'POST':

        # CHECK LOGIN
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Login required'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = ProductSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save(farmer = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([])
def product_detail(request, id):

    try:
        product = Product.objects.get(id=id)

    except Product.DoesNotExist:

        return Response(
            {'error': 'Product not found'},
            status=404
        )

    if request.method == 'GET':

        serializer = ProductSerializer(product)

        return Response(serializer.data)

    elif request.method == 'PUT':

        serializer = ProductSerializer(
            product,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':

        product.delete()

        return Response(
            {'message': 'Deleted successfully'},
            status=204
        )