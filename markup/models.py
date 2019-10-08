from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin


class MainUser(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.id}: {self.username}'


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, default='none')
    address = models.CharField(max_length=300, default='none')
    avatar = models.FileField(default='Images/Default.png')

    def __str__(self):
        return f'{self.user.username}'


class Label(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f'{self.id}:{self.name}'


class Folder(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=3000)
    allowed = models.ManyToManyField(MainUser)  # ???
    folder = models.ForeignKey('self', on_delete=models.CASCADE, default=1, related_name='subfolders', blank=True,
                               null=True)

    class Meta:
        verbose_name = 'Folder'
        verbose_name_plural = 'Folders'

    def __str__(self):
        return f'{self.id}:{self.name}'


def file_save_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'category_{0}/{1}'.format(instance.category.id, filename)


class Image(models.Model):
    name = models.CharField(max_length=150)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='images')
    file = models.FileField(blank=False, null=False, upload_to=file_save_path)

    def __str__(self):
        return f'{self.file.name}'


class PolygonManager(models.Manager):
    def for_user(self, user):
        return self.filter(created_by=user)


class Polygon(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    label = models.ForeignKey(Label, on_delete=models.CASCADE, default=1)
    attributes = models.CharField(max_length=3000)
    points = models.CharField(max_length=5000)
    created_by = models.ForeignKey(MainUser, on_delete=models.CASCADE, default=2)
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


class Comment(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=3000)
    created_by = models.ForeignKey(MainUser, on_delete=models.CASCADE, default=2)
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
