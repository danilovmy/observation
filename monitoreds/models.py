from django.db.models import Model, CharField
from settings import translator as _


class Monitored(Model):

    class Meta:
        verbose_name = _('Monitored')
        verbose_name_plural = _('Monitoreds')
        default_related_name = 'monitoreds'

    first_name = CharField(_('First name'), max_length=255, blank=True, null=True)
