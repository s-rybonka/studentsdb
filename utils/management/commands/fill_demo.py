from django.core.management.base import BaseCommand

from accounts.models import Account
from accounts.tests.factories import AccountFactory
from students.models.group import Group
from students.models.student import Student
from students.tests.factories import StudentFactory


class Command(BaseCommand):
    help = 'Fill Demo'

    def handle(self, *args, **options):
        # Delete existing Account instances if exists
        Account.objects.all().delete()
        # Create new Accounts
        for account in range(50):
            AccountFactory(is_email_confirmed=True)

        # Create superuser
        AccountFactory(
            email='admin@example.com',
            first_name='Admin',
            last_name='Admin',
            is_staff=True,
            is_superuser=True,
            is_email_confirmed=True,
        )
        self.stdout.write(self.style.SUCCESS('Successful created accounts'))

        # Delete students if exist
        student_list = Student.objects.all()
        if student_list:
            student_list.delete()

        # Delete students if exist
        group_list = Group.objects.all()
        if group_list:
            group_list.delete()

        # Create Students and Groups
        for key in range(20):
            # Avoid circular imports by this way
            student = StudentFactory(student_group=None)
            leader = StudentFactory(student_group__leader=student)
            # Assign new group to Leader
            student.student_group = leader.student_group
            student.save()
            # Create student and assign them group with existing leader
            StudentFactory.create_batch(15, student_group=leader.student_group)
        self.stdout.write(self.style.SUCCESS('Successful created students and groups'))