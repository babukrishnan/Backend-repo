import random

from django.contrib.auth.models import User

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from .otpModel import OTP
from .profileModel import FarmerProfile

@api_view(['POST'])
def send_otp(request):

    phone = request.data.get('phone')

    otp = str(random.randint(100000, 999999))

    OTP.objects.create(
        phone=phone,
        otp=otp
    )

    print('OTP:', otp)

    return Response({
        'message': 'OTP sent'
    })

@api_view(['POST'])
def verify_otp(request):

    phone = request.data.get('phone')
    otp = request.data.get('otp')

    otp_obj = OTP.objects.filter(
        phone=phone,
        otp=otp
    ).last()

    if not otp_obj:
        return Response({
            'error': 'Invalid OTP'
        }, status=400)

    # OPTIONAL: delete OTP after use (security)
    OTP.objects.filter(phone=phone).delete()

    username = phone

    # CREATE USER IF NOT EXISTS
    user, created = User.objects.get_or_create(
        username=username
    )

    if created:
        user.set_password(phone)
        user.save()

        # ✅ ALWAYS ensure profile exists (VERY IMPORTANT FIX)
        profile, profile_created = FarmerProfile.objects.get_or_create(
        user=user,
        defaults={
            "name": "New Farmer",
            "phone": phone,
            "village": "",
            "district": ""
        }
    )

    refresh = RefreshToken.for_user(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user_id': user.id
    })