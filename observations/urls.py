from rest_framework.routers import DefaultRouter
from .views import ObservationsViewSet, ObservationViewSet, LastObservationsView
from django.urls import path, include


urlpatterns = [
    # i dont like this solution, should be discussed
    path('observations/last/', LastObservationsView.as_view(), name='last_observation')
]

router = DefaultRouter()
router.register(r'observations', ObservationViewSet, basename='observations')
router.register(r'observation', ObservationViewSet, basename='observation')
urlpatterns += router.urls
