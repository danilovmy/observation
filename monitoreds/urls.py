from rest_framework.routers import DefaultRouter
from .views import MonitoredViewSet, MonitoredsViewSet, MonitoredObservationsViewSet, CalculateViewSet

router = DefaultRouter()
router.register(r'monitoreds', MonitoredsViewSet, basename='monitoreds')
router.register(r'monitored', MonitoredViewSet, basename='monitored')
router.register(r'monitored/(?P<monitored_id>\d+)/observations/(?P<observation_name>\w+)', MonitoredObservationsViewSet, basename='monitored_observations')
router.register(r'monitored/(?P<monitored_id>\d+)/observations/(?P<observation_name>\w+)/calculate', CalculateViewSet, basename='calculated_monitored_observations')

urlpatterns = router.urls