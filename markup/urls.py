from django.conf.urls import url
from django.urls import path
from .views import *
from rest_framework import routers
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

schema_view = get_schema_view(
    openapi.Info(
        title="SkyMed Labelling API",
        default_version='v1',
        description="An open-source markup tool, which can be deployed on your server very quickly"
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser,)
)
urlpatterns = [

    path('token/', obtain_jwt_token, name='api_token_auth'),
    path('token-refresh/', refresh_jwt_token, name='api_token_refresh'),
    url(r'^help/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
router = routers.DefaultRouter()
router.register('folders', FolderViewSet, base_name='folders')
router.register('image_packs', ImagePackViewSet, base_name='image_packs')
# router.register('images', ImageViewSet, base_name='images')
# router.register('allowed_folders', AllowedFolderViewSet, base_name='allowed_folders')
# router.register('polygons', PolygonViewSet, base_name='polygons')
# router.register('labels', LabelViewSet, base_name='labels')
# router.register('comments', CommentViewSet, base_name='comments')
router.register('users', UserViewSet, base_name='users')
router.register('profiles', ProfileViewSet, base_name='profiles')
urlpatterns += router.urls
