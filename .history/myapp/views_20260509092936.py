from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .productModel import Product
from .serializers import ProductSerializer


@api_view(['GET', 'POST'])
@permission_classes([]) # Allow any user to access this view (no authentication required)
def get_products(request):

    if request.method == 'GET':

        products = Product.objects.all()

        serializer = ProductSerializer(
            products,
            many=True
        )

        return Response(serializer.data)

    elif request.method == 'POST':

        serializer = ProductSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
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