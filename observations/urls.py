from rest_framework.routers import DefaultRouter
from .views import ObservationsViewSet, ObservationViewSet, CalculateViewSet


router = DefaultRouter()
router.register(r'observations/calculate', CalculateViewSet, basename='calculations')
router.register(r'observations', ObservationsViewSet, basename='observations')
router.register(r'observation', ObservationViewSet, basename='observation')
urlpatterns = router.urls
