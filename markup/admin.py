from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from markup.models import *


class InlineProfile(admin.StackedInline):
    model = Profile
    verbose_name = 'Profile'
    verbose_name_plural = 'Profiles'
    can_delete = False


class InlineFolders(admin.StackedInline):
    model = AllowedFolder
    verbose_name = 'folder'
    verbose_name_plural = 'folders'
    can_delete = False


@admin.register(MainUser)
class MainUserAdmin(UserAdmin):
    inlines = [InlineProfile, InlineFolders]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'bio', 'address', 'user', 'avatar')


@admin.register(AllowedFolder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('id', 'folder', 'user',)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'file', 'folder_name', 'folder_id')

    def folder_name(self, obj):
        return obj.folder.name

    def folder_id(self, obj):
        return obj.folder.id

    folder_name.admin_order_field = 'Folder name'  # Allows column order sorting
    folder_name.short_description = 'Folder Name'  # Renames column head

    folder_id.admin_order_field = 'Folder id'  # Allows column order sorting
    folder_id.short_description = 'Folder id'  # Renames column head


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
    list_display = ('id', 'name', 'description', 'parent', 'type')
