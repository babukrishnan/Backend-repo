from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from .profileModel import FarmerProfile


# GENERATE JWT TOKENS

def get_tokens(user):

    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }

@api_view(['POST'])
def signup(request):

    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:

        return Response({
            'error': 'Email and password required'
        }, status=400)

    # CHECK USER EXISTS

    if User.objects.filter(username=email).exists():

        return Response({
            'error': 'User already exists'
        }, status=400)

    # CREATE USER

    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
    )

    tokens = get_tokens(user)

    return Response({
        **tokens,
        'is_new_user': True,
    })


@api_view(['POST'])
def login(request):

    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:

        return Response({
            'error': 'Email and Password required'
        }, status=400)

    user = authenticate(
        username=email,
        password=password
    )

    if not user:

        return Response({
            'error': 'Invalid credentials'
        }, status=400)

    profile_exists = FarmerProfile.objects.filter(
        user=user,
        is_completed=True
    ).exists()

    refresh = RefreshToken.for_user(user)

    tokens = get_tokens(user)

    return Response({
        **tokens,
        'is_new_user': not profile_exists,
    })