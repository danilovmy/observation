from rest_framework.routers import DefaultRouter
from .views import ObservationsViewSet, ObservationViewSet
from django.urls import path, include


router = DefaultRouter()
router.register(r'observations', ObservationsViewSet, basename='observations')
router.register(r'observation', ObservationViewSet, basename='observation')
urlpatterns = router.urls
