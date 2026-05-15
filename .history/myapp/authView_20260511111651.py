import random

from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from .otpModel import OTP
from .profileModel import FarmerProfile

@api_view(['POST'])
def verify_otp(request):

    phone = request.data.get('phone')
    otp = request.data.get('otp')
    name = request.data.get('name')

    otp_obj = OTP.objects.filter(
        phone=phone,
        otp=otp
    ).last()

    if not otp_obj:
        return Response({'error': 'Invalid OTP'}, status=400)

    OTP.objects.filter(phone=phone).delete()

    user, created = User.objects.get_or_create(username=phone)

    if created:
        user.set_password(phone)
        user.save()

    # ✅ ALWAYS define profile_created (IMPORTANT FIX)
    profile, profile_created = FarmerProfile.objects.get_or_create(
        user=user,
        defaults={
            "name": name if name else "",
            "phone": phone,
            "village": "",
            "district": ""
        }
    )

    # Optional: update name if provided later
    if name and not profile.name:
        profile.name = name
        profile.save()

    refresh = RefreshToken.for_user(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user_id': user.id,
        'profile_created': profile_created  # ✅ now always safe
    })