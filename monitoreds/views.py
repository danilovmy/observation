from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.serializers import ModelSerializer
from .models import Monitored
from observations.views import ObservationSerializer
from rest_framework.decorators import action

class MonitoredSerializer(ModelSerializer):

    class Meta:
        model = Monitored
        fields = '__all__'


class MonitoredsViewSet(mixins.ListModelMixin, GenericViewSet):
    http_method_names = ['get', 'options', 'head']
    serializer_class = MonitoredSerializer
    queryset = MonitoredSerializer.Meta.model.objects


class MonitoredViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,GenericViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'options', 'head']
    serializer_class = MonitoredSerializer
    queryset = MonitoredSerializer.Meta.model.objects



class MonitoredObservationsViewSet(mixins.ListModelMixin, GenericViewSet):
    http_method_names = ['get', 'options', 'head']
    serializer_class = ObservationSerializer
    queryset = MonitoredSerializer.Meta.model.observations.rel.related_model.objects

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(**self.kwargs)


class CalculateViewSet(MonitoredObservationsViewSet):

    def filter_queryset(self, *args, **kwargs):
        queryset = super().filter_queryset(*args, **kwargs)
        return getattr(queryset, f'get_{self.action}', queryset.get_all)(self, *args, **kwargs)

    @action(detail=False)
    def min(self, *args, **kwargs):
        return self.list(*args, **kwargs)

    @action(detail=False)
    def max(self, *args, **kwargs):
        return self.list(*args, **kwargs)

    @action(detail=False)
    def average(self, *args, **kwargs):
        return self.list(*args, **kwargs)

    @action(detail=False)
    def last(self, *args, **kwargs):
        return self.list(*args, **kwargs)
