import logging

from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import *
from rest_framework.decorators import action
from markup.serializers import *
from markup.models import *

user_logger = logging.getLogger('user_logger')
actions_logger = logging.getLogger('actions_logger')


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = MainUser.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return Profile.objects.all()
