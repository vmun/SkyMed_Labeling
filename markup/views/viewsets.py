import logging

from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from markup.serializers import *
from markup.models import *

user_logger = logging.getLogger('user_logger')
actions_logger = logging.getLogger('actions_logger')

class FolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    # permission_classes = (IsAuthenticated, )

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


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    # permission_classes = (IsAuthenticated, )

    @action(methods=['GET'], detail=True)
    def polygons(self, request, pk):
        # permission: admin
        polygons = Image.objects.get(id=pk).polygons.all()
        serializer = ImageSerializer(polygons, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def my_polygons(self, request, pk):
        # permission: auth
        polygons = Image.objects.get(id=pk).polygons.filter(created_by=self.request.user)
        serializer = ImageSerializer(polygons, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def comments(self, request, pk):
        # permission: admin
        comments = Image.objects.get(id=pk).comments.all()
        serializer = FolderSerializer(comments, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def my_comment(self, request, pk):
        # permission: admin
        comment = Image.objects.get(id=pk).comments.get(created_by=self.request.user)
        serializer = FolderSerializer(comment)
        return Response(serializer.data)
