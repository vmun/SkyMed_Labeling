import logging

from rest_framework.parsers import *
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import *
from rest_framework.decorators import action
from markup.serializers import *
from markup.models import *

user_logger = logging.getLogger('user_logger')
actions_logger = logging.getLogger('actions_logger')


class UserViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = MainUser.objects.all()

    def get_permissions(self):
        if self.action in ['create']:
            return []
        else:
            return [IsAuthenticated(), ]

    @action(methods=['GET'], detail=False)
    def is_admin(self, request):
        return Response({self.request.user.is_superuser}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def set_password(self, request):
        serializer = PasswordSerializer(data=request.data)
        user = self.request.user
        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ['Wrong password.']},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response({'status': 'password set'}, status=status.HTTP_200_OK)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = ProfileSerializer
    # queryset = Profile.objects.all()
    parser_classes = (MultiPartParser, FormParser, JSONParser,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Profile.objects.all()
        else:
            return Profile.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ['me', 'update']:
            return [IsAuthenticated(), ]
        else:
            return [IsAdminUser(), ]

    @action(methods=['GET'], detail=False)
    def me(self, request):
        serializer = self.get_serializer(request.user.profile)
        return Response(serializer.data)
