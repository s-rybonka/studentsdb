import logging


from django.db.models.signals import post_save, post_delete
from django.core.signals import request_started
from django.dispatch import receiver
from django import dispatch
from django.utils.translation import ugettext as _

from .models import Student, Group, Exam


@receiver(post_save, sender=Student)
def log_student_updated_added_event(sender, **kwargs):
    '''Writes info abount newly added or updated student into log file'''
    logger = logging.getLogger(__name__)

    student = kwargs['instance']
    if kwargs['created']:
        logger.info(_('Student added:{} {} (ID:{})').format(student.first_name, student.last_name, student.id))
    else:
        logger.info(_('Student updated:{} {} (ID:{})').format(student.first_name, student.last_name, student.id))


@receiver(post_delete, sender=Student)
def log_student_deleted_event(sender, **kwargs):
    '''Writes info abount deleted student into log file'''

    logger = logging.getLogger(__name__)

    student = kwargs['instance']
    logger.info(_('Student deleted:{} {} (ID:{})').format(student.first_name, student.last_name, student.id))


@receiver(post_save, sender=Group)
def log_group_updated_added_event(sender, **kwargs):
    '''Writes info abount newly added or updated group into log file'''
    logger = logging.getLogger(__name__)
    group = kwargs['instance']
    if kwargs['created']:
        logger.info(_('Group added, title:{} (ID:{})').format(group.title, group.id))
    else:
        logger.info(_('Group updated, title:{} (ID:{})').format(group.title, group.id))


@receiver(post_delete, sender=Group)
def log_group_deleted_event(sender, **kwargs):
    '''Writes info abount deleted group into log file'''

    logger = logging.getLogger(__name__)

    group = kwargs['instance']
    logger.info(_('Group deleted, title:{} (ID:{})').format(group.title, group.id))


@receiver(post_save, sender=Exam)
def log_exam_updated_added_event(sender, **kwargs):
    '''Writes info abount newly added or updated Exam into log file'''
    logger = logging.getLogger(__name__)
    exam = kwargs['instance']

    if kwargs['created']:
        logger.info(_('Exam was added, discipline:{} (ID:{})').format(exam.discipline_name, exam.id))
    else:
        logger.info(_('Exam was updated, discipline:{} (ID:{})').format(exam.discipline_name, exam.id))


@receiver(post_delete, sender=Exam)
def log_exam_deleted_event(sender, **kwargs):
    '''Writes info abount deleted Exam into log file'''

    logger = logging.getLogger(__name__)

    exam = kwargs['instance']
    logger.info(_('Exam was deleted, discipline:{} (ID:{})').format(exam.discipline_name, exam.id))


contact_admin_signal = dispatch.Signal(providing_args=["from_email"])


@receiver(contact_admin_signal)
def contact_admin_signal_handler(sender, **kwargs):
    email = kwargs.get('from_email')

    logger = logging.getLogger(__name__)

    logger.info(_('Email successful sended to administration, user email: {}').format(email))


def log_migrate(sender, **kwargs):
    log = kwargs['plan']
    db_info = kwargs['using']
    app_label = kwargs['app_config'].label

    if log:
        logger = logging.getLogger(__name__)

        logger.info(_('Database:{}. App:{}. Migration apllied: {}').format(db_info, app_label, log))


request_counter = 0

@receiver(request_started)
def count_request(sender, **kwargs):
    global request_counter
    if request_started:
        request_counter += 1
        logger = logging.getLogger(__name__)

        logger.info(_('Requests amount on site: {}').format(request_counter))
