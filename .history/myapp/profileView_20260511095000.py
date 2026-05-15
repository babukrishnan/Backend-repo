from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework import status

from django.contrib.auth.models import User

from .profileModel import FarmerProfile
from .serializers import FarmerProfileSerializer

@api_view(['GET', 'PUT'])
def profile_detail(request):

     # CHECK LOGIN

    if not request.user.is_authenticated:

        return Response(
            {'error': 'User not authenticated'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:

        profile = FarmerProfile.objects.get(
            user=request.user
        )

    except FarmerProfile.DoesNotExist:

        return Response(
            {'error': 'Profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    # GET PROFILE

    if request.method == 'GET':

        serializer = FarmerProfileSerializer(profile)

        return Response(serializer.data)

    # UPDATE PROFILE

    elif request.method == 'PUT':

        serializer = FarmerProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )