from django.db.models import ForeignKey, DateTimeField, CharField, CASCADE, Model, QuerySet, FloatField
from settings import translator as _
from django.db.models.expressions import Value, F
from django.db.models.aggregates import Avg

class ObservationQueryset(QuerySet):

    def transform_value(self, *args, **kwargs):
        # ouput_field should be defined accordingly to the value_type, not always float
        return self.annotate(transformed_value=Value(F('value'), output_field=FloatField()))

    def get_min(self, *args, **kwargs):
        return self.transform_value(*args, **kwargs).order_by('transformed_value')[:1]

    def get_max(self, *args, **kwargs):
        return self.transform_value(*args, **kwargs).order_by('-transformed_value')[:1]

    def get_average(self, *args, **kwargs):
        return self.transform_value(*args, **kwargs).aggregate(Avg('transformed_value'))

    def get_last(self, *args, **kwargs):
        return self.order_by('-issued')[:1]

    def get_all(self, *args, **kwargs):
        return self.all()


class Observation(Model):

    class Meta:
        verbose_name = _('Observation')
        verbose_name_plural = _('Observations')
        default_related_name = 'observations'

    monitored = ForeignKey('monitoreds.Monitored', on_delete=CASCADE)
    observation_name = CharField(_('Observation name'), max_length=255, blank=True, null=True)
    issued = DateTimeField(_('Issued'), blank=True, null=True)
    value = CharField(_('Text'), max_length=255, blank=True, null=True)
    value_type = CharField(_('Type of value'), max_length=255, blank=True, null=True)
    value_unit = CharField(_('Measure units of value'), max_length=255, blank=True, null=True)
    observation = ForeignKey('self', verbose_name=_('Observation Components'), related_name = 'components', on_delete=CASCADE, null=True, blank=True)
    objects = ObservationQueryset.as_manager()
