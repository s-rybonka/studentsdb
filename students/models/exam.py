from django.utils.translation import ugettext as _

from django.db import models


class Exam(models.Model):
    discipline_name = models.CharField(max_length=256, verbose_name=_('Discipline name'), blank=False)
    date = models.DateTimeField(verbose_name=_('Date'), blank=False)
    teacher_name = models.CharField(max_length=256, verbose_name=_('Teacher name'), blank=False)
    group_id = models.ForeignKey('Group', verbose_name=_('Group'), blank=True, null=True)

    class Meta(object):
        verbose_name = _('Exam')
        verbose_name_plural = _('Exams')

    def __str__(self):
        return '{}'.format(self.discipline_name)


class ExamResult(models.Model):
    exam_id = models.ForeignKey('Exam', verbose_name=_('Exam'), blank=True)
    student_id = models.ForeignKey('Student', verbose_name=_('Student'), blank=True)
    rating = models.FloatField(verbose_name='Rating', blank=False)
    date = models.DateField(verbose_name='Date', blank=False)

    class Meta(object):
        verbose_name = _('Exam Result')
        verbose_name_plural = _('Exam Results')

    def __str__(self):
        return '{}'.format(self.exam_id)
