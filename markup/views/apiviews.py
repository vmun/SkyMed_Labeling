from markup.models import *
from markup.serializers import *
from rest_framework import generics
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class PolygonList(generics.CreateAPIView):
    queryset = Polygon.objects.all()
    permission_classes = {IsAuthenticated, }
    serializer_class = PolygonSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CommentList(generics.CreateAPIView):
    permission_classes = {IsAuthenticated, }
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class LabelList(generics.ListCreateAPIView):
    permission_classes = {IsAuthenticated, }
    queryset = Label.objects.all()
    serializer_class = LabelSerializer


class ImageList(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = {IsAuthenticated, }

    def get_queryset(self):
        try:
            imagePack = ImagePack.objects.get(id=self.kwargs.get('pk'))
        except Folder.DoesNotExist:
            raise Http404
        queryset = imagePack.images.all()

        return queryset


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = {IsAuthenticated, }


class CommentsInImage(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        try:
            image = Image.objects.get(id=self.kwargs['pk'])
        except Image.DoesNotExist:
            raise Http404
        queryset = image.comments.filter(created_by=self.request.user)
        return queryset

    def get_serializer_class(self):
        return CommentSerializer


class PolygonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Polygon.objects.all()
    serializer_class = PolygonSerializer
    permission_classes = {IsAuthenticated, }


class PolygonsInImage(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        try:
            image = Image.objects.get(id=self.kwargs['pk'])
        except Image.DoesNotExist:
            raise Http404
        queryset = image.polygons.filter(created_by=self.request.user)
        return queryset

    def get_serializer_class(self):
        return PolygonSerializer
