from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from markup.models import Image, Polygon, Comment, Label, Folder, Profile, MainUser


class InlineProfile(admin.StackedInline):
    model = Profile
    verbose_name = 'Profile'
    verbose_name_plural = 'Profiles'
    can_delete = False


@admin.register(MainUser)
class MainUserAdmin(UserAdmin):
    inlines = [InlineProfile, ]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'bio', 'address', 'user', 'avatar')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'file', 'category_name', 'category_id')

    def category_name(self, obj):
        return obj.folder.name

    def category_id(self, obj):
        return obj.folder.id

    category_name.admin_order_field = 'Category name'  # Allows column order sorting
    category_name.short_description = 'Category Name'  # Renames column head

    category_id.admin_order_field = 'Category id'  # Allows column order sorting
    category_id.short_description = 'Category id'  # Renames column head


@admin.register(Polygon)
class PolygonAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_created', 'label', 'image', 'created_by', 'text')


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_created', 'created_by', 'text', 'image', 'parent')


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'parent', 'type')
