import logging
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import *
from rest_framework.decorators import action
from markup.serializers import *
from markup.models import *

user_logger = logging.getLogger('user_logger')
actions_logger = logging.getLogger('actions_logger')


class FolderViewSet(viewsets.ModelViewSet):
    serializer_class = FolderSerializer

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'create', 'partial_update']:
            return [IsAdminUser(), ]
        else:
            return [IsAuthenticated(), ]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Folder.objects.all()
        else:
            return self.request.user.folders

    @action(methods=['GET'], detail=False)
    def my(self, request):
        # permission: auth
        folders = Folder.objects.filter(allowed=self.request.user)
        serializer = self.get_serializer(folders, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def subfolders(self, request, pk):
        # permission: admin
        subfolders = Folder.objects.get(id=pk).subfolders.all()
        serializer = FolderSerializer(subfolders, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def my_subfolders(self, request, pk):
        # permission: auth
        subfolders = Folder.objects.get(id=pk).subfolders.filter(allowed=self.request.user)
        serializer = FolderSerializer(subfolders, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def images(self, request, pk):
        # permission: auth, have_access
        images = Folder.objects.get(id=pk).images.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)


class AllowedFolderViewSet(viewsets.ModelViewSet):
    queryset = AllowedFolder.objects.all()
    serializer_class = AllowedFolderSerializer
    permission_classes = (IsAdminUser,)
