from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework import status

from django.contrib.auth.models import User

from .profileModel import FarmerProfile
from .serializers import FarmerProfileSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_profile(request):

    user = request.user

    # Create profile if not exists
    profile, created = FarmerProfile.objects.get_or_create(
        user=user
    )

    # Get data from frontend
    profile.name = request.data.get('name')
    profile.village = request.data.get('village')
    profile.district = request.data.get('district')

    # Optional profile image
    if request.FILES.get('profile_image'):
        profile.profile_image = request.FILES.get(
            'profile_image'
        )

    # Mark onboarding complete
    profile.is_completed = True

    profile.save()

    return Response({
        'message': 'Profile completed successfully'
    })


# GET / UPDATE PROFILE
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_detail(request):
    

    print("USER:", request.user)
    print("AUTH:", request.auth)
     # CHECK LOGIN

    try:

        profile = FarmerProfile.objects.get(
            user=request.user
        )

    except FarmerProfile.DoesNotExist:

        return Response(
            {'error': 'Profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    # ==============================
    # GET PROFILE
    # ==============================

    if request.method == 'GET':

        serializer = FarmerProfileSerializer(
            profile
        )

        return Response(serializer.data)

    # ==============================
    # UPDATE PROFILE
    # ==============================

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