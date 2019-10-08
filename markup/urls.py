from .views import FolderViewSet, ImageViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('folders', FolderViewSet, base_name='api')
router.register('images', ImageViewSet, base_name='api')

urlpatterns = router.urls