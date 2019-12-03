from rest_framework import serializers
from django.contrib.auth.models import User
from markup.models import *


class UserShortSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = MainUser
        fields = ('id', 'username', 'first_name', 'email', 'is_superuser')


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = MainUser
        fields = ('id', 'username', 'password', 'email',)
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = MainUser.objects.create_user(**validated_data)
        return user


class PasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    origin = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('id', 'origin', 'bio', 'address', 'avatar')

    def get_origin(self, obj):
        if obj.user is not None:
            return obj.user.username + " with id " + str(obj.user.id)
        return ''


class SubFolderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Folder
        fields = ('id', 'name', 'description', 'type',)


class FolderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Folder
        fields = ('id', 'name', 'description', 'parent')


class ImagePackSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Folder
        fields = ('id', 'name', 'description', 'parent')


class AdminFolderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Folder
        fields = ('id', 'name', 'description', 'type', 'parent')


class AllowedImagePackSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = AllowedImagePack
        fields = ('id', 'user', 'imagePack',)


class LabelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = Label
        fields = '__all__'


class PolygonSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(required=False, allow_blank=True)
    name = serializers.SerializerMethodField()

    class Meta:
        model = Polygon
        fields = ('id', 'name', 'label', 'text', 'points', 'image')

    def get_name(self, obj):
        return obj.label.name


class ImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    # extra = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('id', 'name', 'file')

    # def get_extra(self, obj):
    #     polygons = obj.polygons.filter(created_by=self.context.get('request').user)
    #     if polygons:
    #         return True
    #     return False


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(required=True, allow_blank=False)
    date_created = serializers.DateTimeField(read_only=True)
    creator_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'text', 'date_created', 'image', 'creator_name')

    def get_creator_name(self, obj):
        return obj.created_by.username
