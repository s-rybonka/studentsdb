from __future__ import unicode_literals

from django.utils.translation import ugettext as _

from django.db import models
from .group import Group


class Student(models.Model):
    '''Student model'''

    first_name = models.CharField(max_length=256, blank=False, verbose_name=_('Name'))
    last_name = models.CharField(max_length=256, blank=False, verbose_name=_('Surname'))
    middle_name = models.CharField(max_length=256, blank=True, verbose_name=_('Second name'), default='')
    birthday = models.DateField(blank=False, verbose_name=_('Date of birthday'), null=True)
    photo = models.ImageField(blank=True, verbose_name='Foto', null=True, upload_to='media')
    ticket = models.CharField(max_length=256, blank=False, verbose_name=_('Ticket'))
    notes = models.TextField(blank=True, verbose_name=_('Additional notices'), null=True)
    student_group = models.ForeignKey(Group, verbose_name=_('Group'), blank=False, null=True, on_delete=models.PROTECT)

    class Meta(object):
        verbose_name = _('Student')
        verbose_name_plural = _('Students')
        ordering = ['last_name']

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
