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
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return []
        else:
            return [IsAuthenticated(), ]

    def get_queryset(self):
        if self.action in ['create']:
            return MainUser.objects.all()
        else:
            return MainUser.objects.filter(user=self.request.user)

    @action(methods=['Post'], detail=False)
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


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return Profile.objects.all()
