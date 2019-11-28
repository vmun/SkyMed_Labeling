from .views import *
from rest_framework import routers

urlpatterns = [
]
router = routers.DefaultRouter()
router.register('folders', FolderViewSet, base_name='folders')
# router.register('images', ImageViewSet, base_name='api')
router.register('register', UserViewSet, base_name='register')
router.register('profiles', ProfileViewSet, base_name='profiles')
urlpatterns += router.urls
