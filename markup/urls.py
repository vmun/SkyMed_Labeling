from django.conf.urls import url
from django.urls import path
from markup import views
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

    path('login/', obtain_jwt_token, name='api_token_auth'),
    path('token-refresh/', refresh_jwt_token, name='api_token_refresh'),
    path('register/', views.register),
    url(r'^help/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('polygon/', views.PolygonList.as_view()),  # Add polygons
    path('polygon/<int:pk>/', views.PolygonDetail.as_view()),  # Delete polygon at PK
    # path('image_packs/<int:pk>/', views.ImageList.as_view()),  # Show images in category PK
    # path('image/<int:pk>/polygons/', views.PolygonsInImage.as_view()),  # Show polygons in image PK
    path('comment/', views.CommentList.as_view()),  # Add comments
    path('comment/<int:pk>/', views.CommentDetail.as_view()),  # Delete/show comment at PK
    # path('image/<int:pk>/comments/', views.CommentsInImage.as_view()),  # Show comments in image PK
    path('labels/', views.LabelList.as_view()),  # lists labels
]

router = routers.DefaultRouter()
router.register('folders', views.FolderViewSet, base_name='folders')
router.register('image_packs', views.ImagePackViewSet, base_name='image_packs')
router.register('allow_pack', views.AllowedImagePackViewSet, base_name='allow_pack')
router.register('images', views.ImageViewSet, base_name='images')
# router.register('polygons', views.PolygonViewSet, base_name='polygons')
# router.register('labels', views.LabelViewSet, base_name='labels')
# router.register('comments', views.CommentViewSet, base_name='comments')
router.register('users', views.UserViewSet, base_name='users')
router.register('profiles', views.ProfileViewSet, base_name='profiles')
urlpatterns += router.urls
