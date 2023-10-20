from django.db.models import ForeignKey, DateTimeField, CharField, CASCADE, Model, QuerySet
from settings import translator as _


class ObservationQueryset(QuerySet):
    ...

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
