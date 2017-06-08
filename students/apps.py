from __future__ import unicode_literals
from django.apps import AppConfig

from django.db.models.signals import post_migrate


class StudentsAppConfig(AppConfig):
    name = 'students'
    verbose_name ='Students DB'

    def ready(self):
        from students import signals
        post_migrate.connect(signals.log_migrate, sender=self)
