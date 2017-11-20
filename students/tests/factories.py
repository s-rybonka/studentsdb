import datetime

import factory

from students.models.group import Group
from students.models.student import Student


class StudentFactory(factory.DjangoModelFactory):
    """
    Student Factory
    """

    class Meta:
        model = Student

    student = factory.SubFactory('accounts.tests.factories.AccountFactory')
    first_name = factory.Sequence(lambda n: 'First_name_%s' % n)
    last_name = factory.Sequence(lambda n: 'Last_name_%s' % n)
    middle_name = factory.Sequence(lambda n: 'Middle_name_%s' % n)
    birthday = factory.LazyFunction(datetime.datetime.now)
    ticket = factory.Sequence(lambda n: '%d' % n)
    notes = factory.Sequence(lambda n: 'Additional_Info_%s' % n)
    student_group = factory.SubFactory('students.tests.factories.GroupFactory')


class GroupFactory(factory.DjangoModelFactory):
    """
    Group Factory
    """

    class Meta:
        model = Group

    title = factory.Sequence(lambda n: 'Group_%s' % n)
    leader = factory.SubFactory(StudentFactory)
    notes = factory.Sequence(lambda n: 'Notes_%s' % n)




