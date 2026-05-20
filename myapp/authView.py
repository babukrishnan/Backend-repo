from google.oauth2 import id_token
from google.auth.transport import requests

from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from .profileModel import FarmerProfile

@api_view(['POST'])
def firebase_login(request):

    id_token = request.data.get('idToken')

    try:
        # Verify Google Token
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request()
        )
        email = idinfo['email']
        name = idinfo.get('name', '')

        # Create User
        user, created = User.objects.get_or_create(
                username=email,
                defaults={
                    'email': email,
                    'first_name': name,
                }
        )

        # Check Profile
        profile_exists = FarmerProfile.objects.filter(
                user=user,
                is_completed=True
            ).exists()

        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'is_new_user': not profile_exists,
        })

    except Exception as e:

        return Response({ 'error': str(e) }, status=400)