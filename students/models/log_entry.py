from django.db import models
from django.utils.translation import ugettext as _


class LogEntry(models.Model):
    error_level = models.CharField(max_length=20, verbose_name=_('Level'))
    date = models.DateTimeField()
    error_message = models.CharField(max_length=1000, verbose_name=_('Messages'))



