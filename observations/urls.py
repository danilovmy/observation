from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import ObservationsViewSet, ObservationViewSet, ComputeObservationsMean

router = DefaultRouter()
router.register(r'observations/<int:monitored>', ObservationsViewSet, basename='observations')
router.register(r'observation', ObservationViewSet, basename='observation')

urlpatterns = router.urls


urlpatterns += [
    # path('compute/mean/{observation_name}', ComputeObservationsMean.as_view({'get': 'list'})), #  can add monitored or data in query
    # path('compute/average/{observation_name}', ...), #  can add monitored or data in query
    # path('compute/max/{observation_name}', ... ), #  can add monitored or data in query
    # path('compute/min/{observation_name}', ... ), #  can add monitored or data in query
]
