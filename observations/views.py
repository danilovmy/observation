from rest_framework.viewsets import ModelViewSet, mixins, GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view
from django_filters import rest_framework as filters
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Observation


# class ObservationsFilter(BaseFilterBackend):

#     def filter_queryset(self, request, queryset, view):
#         kwargs = dict(observation_name=request.query_params.get('observation_name'),
#                       monitored_id = request.query_params.get('monitored_id'),
#                       issued__lte = request.query_params.get('issued_from'),
#                       issued__gte = request.query_params.get('issued_till'))
#         kwargs = {key: val for key, val in kwargs.items() if val} or {'observation__isnull': True}
#         return queryset if view.kwargs else queryset.filter(**kwargs)


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


@extend_schema_view(list=extend_schema(description='get last from list of observations'))
class LastObservationsView(ListAPIView):
    http_method_names = ['get', 'options', 'head']
    serializer_class = ObservationSerializer
    queryset = ObservationSerializer.Meta.model.objects
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ObservationsFilter

    def filter_queryset(self, *args, **kwargs):
        return super().filter_queryset(*args, **kwargs).order_by('-issued')[:1]


class ObservationViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,GenericViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'options', 'head']
    serializer_class = ObservationSerializer
    queryset = ObservationSerializer.Meta.model.objects


# # details lists

# async def get_observations_by(observation_name: str, monitored_id: int=None, date_from: datetime=None, date_till: datetime=None):
#     logger.info(f"get observations {observation_name}")
#     return await Observation.objects.filter(observation_name=observation_name, monitored_id=monitored_id, date_from=date_from, date_till=date_till)

# # computations
# async def get_compute_mean_by(observation_name: str, monitored_id: int=None, date_from: datetime=None, date_till: datetime=None):
#     logger.info(f"compute observations mean{observation_name}")
#     return await Observation.objects.compute_mean(observation_name=observation_name, monitored_id=monitored_id, date_from=date_from, date_till=date_till)


# async def get_compute_average_by(observation_name: str, monitored_id: int=None, date_from: datetime=None, date_till: datetime=None):
#     logger.info(f"compute observations average{observation_name}")
#     return await Observation.objects.compute_average(observation_name=observation_name, monitored_id=monitored_id, date_from=date_from, date_till=date_till)


# async def get_compute_min_by(observation_name: str, monitored_id: int=None, date_from: datetime=None, date_till: datetime=None):
#     logger.info(f"compute observations min{observation_name}")
#     return await Observation.objects.compute_min(observation_name=observation_name, monitored_id=monitored_id, date_from=date_from, date_till=date_till)


# async def get_compute_max_by(observation_name: str, monitored_id: int=None, date_from: datetime=None, date_till: datetime=None):
#     logger.info(f"compute observations max{observation_name}")
#     return await Observation.objects.compute_max(observation_name=observation_name, monitored_id=monitored_id, date_from=date_from, date_till=date_till)


# # savers / patchers
# async def post_add_observation(observation: Observation):
#     logger.info(f"Add observation {observation}")
#     return await Observation.objects.add(Observation)

# async def patch_change_observation(observation: Observation):
#     # Do nothing, probably it should be not possible to change any observation directly
#     logger.info(f"Update observation {observation}")
#     return await Observation.objects.update(Observation)

# async def delete_observation(observation: Observation):
#     # Do nothing, probably it should be not possible to delete any observation directly
#     logger.info(f"Delete observation {observation}")
#     return await Observation.objects.delete(Observation)
