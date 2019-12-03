from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from markup.serializers import *
from markup.models import *


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)