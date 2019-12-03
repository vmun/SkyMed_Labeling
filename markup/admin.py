from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from markup.models import *


class InlineProfile(admin.StackedInline):
    model = Profile
    verbose_name = 'Profile'
    verbose_name_plural = 'Profiles'
    can_delete = False


class InlineFolders(admin.StackedInline):
    model = AllowedImagePack
    verbose_name = 'folder'
    verbose_name_plural = 'folders'
    can_delete = False


@admin.register(MainUser)
class MainUserAdmin(UserAdmin):
    inlines = [InlineProfile, InlineFolders]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'bio', 'address', 'user', 'avatar')


@admin.register(AllowedImagePack)
class AllowedImagePackAdmin(admin.ModelAdmin):
    list_display = ('id', 'imagePack', 'user',)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'file', 'imagePack_name', 'imagePack_id')

    def imagePack_name(self, obj):
        return obj.imagePack.name

    def imagePack_id(self, obj):
        return obj.imagePack.id

    imagePack_name.admin_order_field = 'Image Pack name'  # Allows column order sorting
    imagePack_name.short_description = 'Image Pack Name'  # Renames column head

    imagePack_id.admin_order_field = 'Image Pack id'  # Allows column order sorting
    imagePack_id.short_description = 'Image Pack id'  # Renames column head


@admin.register(Polygon)
class PolygonAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_created', 'label', 'image', 'created_by', 'text')


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_created', 'created_by', 'text', 'image',)


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'parent')


@admin.register(ImagePack)
class ImagePackAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'parent')
