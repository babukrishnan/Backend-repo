from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .productModel import Product
from .serializers import ProductSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import parser_classes

#test 
def home(request):
    return HttpResponse("Backend Running Successfully 🚀")
    
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
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

        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PRODUCT DETAIL
# ====================================
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def product_detail(request, id):

    try:
        product = Product.objects.get(id=id)

    except Product.DoesNotExist:

        return Response(
            {'error': 'Product not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    # GET SINGLE PRODUCT
    # =========================
    if request.method == 'GET':

        serializer = ProductSerializer(product)

        return Response(serializer.data)

    # UPDATE PRODUCT
    # =========================
    elif request.method == 'PUT':

        # LOGIN REQUIRED
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Login required'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # OWNER CHECK
        if product.farmer != request.user:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )

        data = request.data.copy()
         
        # Remove empty image field
        if 'image' in data and data['image'] == '':
            data.pop('image')

        serializer = ProductSerializer(
            product,
            data=data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE PRODUCT
    # =========================
    elif request.method == 'DELETE':

        # LOGIN REQUIRED
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Login required'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # OWNER CHECK
        if product.farmer != request.user:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )

        product.delete()

        return Response(
            {'message': 'Deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_products(request):

    products = Product.objects.filter(
        farmer=request.user
    ).order_by('-created_at')

    serializer = ProductSerializer(
        products,
        many=True
    )

    return Response(serializer.data)