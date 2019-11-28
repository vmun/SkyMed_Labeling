from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from markup.utils.ChoiceFields import *
from markup.utils.document_upload import *


class MainUser(AbstractUser):
    role = models.IntegerField(choices=ROLES, default=GUEST)
    folders = models.ManyToManyField('Folder', through='AllowedFolder', related_name='participants')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.id}: {self.username}'


class Profile(models.Model):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, default='none')
    address = models.CharField(max_length=300, default='none')
    avatar = models.FileField(default='Default/Default.png')

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.username


class Folder(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=2000)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subfolders', blank=True,
                               null=True)  # parent
    type = models.IntegerField(choices=FOLDER_TYPES, default=ROOT)

    class Meta:
        verbose_name = 'Folder'
        verbose_name_plural = 'Folders'

    def __str__(self):
        return f'{self.id}:{self.name}'


class AllowedFolder(models.Model):
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name="membership")
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="membership")

    class Meta:
        unique_together = ('user', 'folder',)


class Image(models.Model):
    name = models.CharField(max_length=150)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='images')
    file = models.FileField(upload_to=task_document_path, validators=[validate_file_size, validate_extension])

    def __str__(self):
        return f'{self.file.name}'


class Label(models.Model):
    name = models.CharField(max_length=400, unique=True)

    def __str__(self):
        return f'{self.id}:{self.name}'


class Attachments(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=3000)
    created_by = models.ForeignKey(MainUser, on_delete=models.CASCADE, default=1)

    class Meta:
        abstract = True


class PolygonManager(models.Manager):
    def by_user(self, user):
        return self.filter(created_by=user)


class Polygon(Attachments):
    label = models.ForeignKey(Label, on_delete=models.CASCADE, default=1)
    points = models.CharField(max_length=1000)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, default=1, related_name='polygons')

    objects = PolygonManager()

    class Meta:
        verbose_name = 'Polygon'
        verbose_name_plural = 'Polygons'

    def __str__(self):
        return '{}: {}'.format(self.id, self.label.name)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.label.name
        }


class CommentManager(models.Manager):
    def for_user(self, user):
        return self.filter(created_by=user)


class Comment(Attachments):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, default=1, related_name='comments')
    objects = CommentManager()

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return '{}: {}'.format(self.id, self.text)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.text
        }
