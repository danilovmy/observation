from rest_framework.viewsets import ModelViewSet, mixins, GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters import rest_framework as filters
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Observation
from drf_spectacular.utils import OpenApiParameter


class ObservationsFilter(filters.FilterSet):
    observation_name = filters.CharFilter(lookup_expr="icontains")
    monitored = filters.ModelChoiceFilter(queryset=Observation.monitored.field.remote_field.model.objects.all(), required=True)
    issued = filters.IsoDateTimeFromToRangeFilter()

    class Meta:
        model = Observation
        fields = ('observation_name', 'monitored', 'issued')

    @property
    def qs(self):
        qs = super().qs
        return qs if self.form.is_valid() and self.form.cleaned_data.get('observation_name') else qs.filter(observation__isnull=True)


class ObservationSerializer(ModelSerializer):
    monitored_id = serializers.PrimaryKeyRelatedField(source='monitored', queryset=Observation.monitored.field.remote_field.model.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Observation
        fields = "id", "monitored_id", "observation_name", "issued", "value", "value_type", "value_unit", "components"

    def get_fields(self):
        return super().get_fields() | {'components': ObservationSerializer(many=True, required=False, allow_null=True)}


    def create(self, validated_data):
        components_data = validated_data.pop('components')
        observation = self.Meta.model.objects.create(**validated_data)
        static_data = dict(observation=observation, monitored=observation.monitored, issued=observation.issued)
        for component_data in components_data:
            self.Meta.model.objects.create(**component_data, **static_data)
        return observation


@extend_schema_view(list=extend_schema(description='get list of observations'))
class ObservationsViewSet(mixins.ListModelMixin, GenericViewSet):
    http_method_names = ['get', 'options', 'head']
    serializer_class = ObservationSerializer
    queryset = ObservationSerializer.Meta.model.objects
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ObservationsFilter


class ObservationViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,GenericViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'options', 'head']
    serializer_class = ObservationSerializer
    queryset = ObservationSerializer.Meta.model.objects



@extend_schema_view(
    #DRF spectacular dont work with filter_backends and custom action
    last=extend_schema(description='get last from list of observations', parameters = [
        OpenApiParameter(name='observation_name', description="type of observations"),
        OpenApiParameter(name='monitored', description="monitored id"),
        OpenApiParameter(name='issued', description="range of data"),
        ]),
    )
class CalculateViewSet(ObservationsViewSet):

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
