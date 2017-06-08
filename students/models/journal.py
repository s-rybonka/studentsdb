from django.db import models
from django.utils.translation import ugettext as _
from ..models.student import Student


class Journal(models.Model):
    student = models.ForeignKey(Student, max_length=256, verbose_name=_('Student name'), related_name='students',
                                blank=False, unique_for_month='date')
    date = models.DateField(blank=False, verbose_name=_('Date'))
    status = models.BooleanField(default=False, verbose_name=_('Status'))


for i in range(1, 31):
    Journal.add_to_class('present_day_%s' % i, models.BooleanField(default=False))


    class Meta(object):
        verbose_name = _('Journal')
