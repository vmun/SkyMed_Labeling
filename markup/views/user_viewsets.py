import logging

from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.permissions import *

from markup.serializers import *
from markup.models import *

logger = logging.getLogger('user_logger')


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = MainUser.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()
        logger.info(f"{serializer.data.get('username')} registered!\n")
