from rest_framework.routers import DefaultRouter
from services.views import CategoryViewSet, ServiceViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'services', ServiceViewSet, basename='services')

urlpatterns = router.urls
