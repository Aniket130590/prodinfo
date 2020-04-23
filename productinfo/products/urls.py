from rest_framework import routers

from .api import ProductPredictionsViewSet

router = routers.DefaultRouter()
router.register('productinfo', ProductPredictionsViewSet, basename='productinfo')
urlpatterns = router.urls