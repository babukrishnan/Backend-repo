from rest_framework.decorators import api_view
from rest_framework.response import Response

from .profileModel import FarmerProfile
from .serializers import FarmerProfileSerializer

@api_view(['GET', 'PUT'])
def profile_detail(request):
    profile = FarmerProfile.objects.get(user=request.user)

    if request.method == 'GET':
        serializer = FarmerProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = FarmerProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)