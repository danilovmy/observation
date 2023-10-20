from rest_framework.routers import DefaultRouter
from .views import MonitoredViewSet, MonitoredsViewSet

router = DefaultRouter()
router.register(r'monitoreds', MonitoredsViewSet, basename='monitoreds')
router.register(r'monitored', MonitoredViewSet, basename='monitored')

urlpatterns = router.urls