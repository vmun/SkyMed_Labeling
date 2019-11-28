from markup.views.user_viewsets import UserViewSet
from .views import FolderViewSet, ImageViewSet
from rest_framework import routers

urlpatterns = [
]
router = routers.DefaultRouter()
# router.register('folders', FolderViewSet, base_name='api')
# router.register('images', ImageViewSet, base_name='api')
router.register('register', UserViewSet, base_name='register')
urlpatterns += router.urls