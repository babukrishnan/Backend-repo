from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework import status

from django.contrib.auth.models import User

from .profileModel import FarmerProfile
from .serializers import FarmerProfileSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import parser_classes

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def profile_detail(request):

    print(request.data)
    
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

        serializer = FarmerProfileSerializer(
            profile
        )

        return Response(serializer.data)

    # UPDATE PROFILE
    # ==============================
    elif request.method == 'PUT':

        serializer = FarmerProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            updated_profile  = serializer.save()

             # REMOVE IMAGE
            if request.data.get('remove_image') == 'true':
                updated_profile.profile_image.delete(save=True)

                updated_profile.profile_image = None

                updated_profile.save()

            return Response(FarmerProfileSerializer(updated_profile).data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_profile(request):

    print(request.data)

    user = request.user

    # Create profile if not exists
    profile, created = FarmerProfile.objects.get_or_create(
        user=user
    )

    # REQUIRED FIELDS

    name = request.data.get('name')
    phone = request.data.get('phone')
    village = request.data.get('village')
    district = request.data.get('district')

    # VALIDATION

    if not name or not phone or not village or not district:

        return Response({
            'error': 'All required fields must be filled'
        }, status=400)

    # CHECK DUPLICATE PHONE

    phone_exists = FarmerProfile.objects.filter(
        phone=phone
    ).exclude(
        user=user
    ).exists()

    if phone_exists:

        return Response({
            'error': 'Phone number already exists'
        }, status=400)

    # Get data from frontend
    profile.name = name
    profile.phone = phone
    profile.village = village
    profile.district = district

    profile.farming = request.data.get('farming')
    profile.land_size = request.data.get('land_size')

    # Optional profile image
    if request.FILES.get('profile_image'):
        profile.profile_image = request.FILES.get(
            'profile_image'
        )

    # Mark onboarding complete
    profile.is_completed = True

    profile.save()

    serializer = FarmerProfileSerializer(profile)

    return Response(serializer.data)