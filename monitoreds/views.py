from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.serializers import ModelSerializer
from .models import Monitored


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
