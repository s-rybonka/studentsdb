from django.shortcuts import render
from django.views import generic
from ..models.journal import Journal
from ..models.student import Student
from django.shortcuts import reverse
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from calendar import monthrange, weekday, day_abbr
from django.http import JsonResponse

from ..util import paginate, get_current_group


# Manage Journal
class JournalView(generic.TemplateView):
    template_name = "cabinet_/journal/journal.html"

    def get_context_data(self, **kwargs):

        # get context data from TemplateView class

        context = super(JournalView, self).get_context_data(**kwargs)

        # check  if we need to display some specific month
        if self.request.GET.get('month'):

            month = datetime.strptime(self.request.GET.get('month'), '%Y-%m-%d'
                                      ).date()
        else:
            # otherwise just displaying current month data
            today = datetime.today()
            month = date(today.year, today.month, 1)
            print(month)

        # calculate current, previous and next month details
        # we need this for navigation element in template

        next_month = month + relativedelta(months=1)
        prev_month = month - relativedelta(months=1)

        context['prev_month'] = prev_month.strftime('%Y-%m-%d')
        context['next_month'] = next_month.strftime('%Y-%m-%d')
        context['year'] = month.year
        context['month_verbose'] = month.strftime('%B')

        # we'll use this variable in students pagination

        context['cur_month'] = month

        # prepare variable for template to generate
        # journal table header elements

        myear, mmonth = month.year, month.month

        number_of_days = monthrange(myear, mmonth)[1]

        context['month_header'] = [
            {'day': d,
             'verbose': day_abbr[weekday(myear, mmonth, d)][:3]
             } for d in range(1, number_of_days + 1)
            ]

        # get all students from database
        if kwargs.get('pk'):
            queryset = [Student.objects.get(pk=kwargs['pk'])]
        else:
            current_group = get_current_group(self.request)
            if current_group:
                queryset = Student.objects.filter(student_group=current_group)
            else:
                queryset = Student.objects.all().order_by('last_name')

        # url to update student presence, for form post
        update_url = reverse('journal')

        # go over all students and collect data about presence
        # during selected month
        students = []

        for student in queryset:
            # try to get journal object by month selected
            # month and current student

            try:
                journal = Journal.objects.get(student=student, date=month)

            except Exception:
                journal = None

            # fill in days presence list for current student
            days = []
            for day in range(1, number_of_days + 1):
                days.append({
                    'day': day,
                    'present': journal and getattr(journal, 'present_day_%d' % day, False) or False,
                    'date': date(myear, mmonth, day).strftime('%Y-%m-%d'),
                })

            # prepare metadata for current student
            students.append({
                'fullname': '%s %s' % (student.first_name, student.last_name),
                'days': days,
                'id': student.id,
                'update_url': update_url,
            })

            # apply pagination, 10 students per page
        context = paginate(students, 1, self.request, context, var_name='students')

        # finally return updated context
        # with paginated students

        return context

    def post(self, request, *args, **kwargs):
        data = request.POST

        # prepare student, dates and presence data
        current_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        month = date(current_date.year, current_date.month, 1)
        present = data['present'] and True or False
        student = Student.objects.get(pk=data['pk'])

        # get or create object for given student and month
        journal = Journal.objects.get_or_create(student=student, date=month)[0]

        # set new presence on journal for given student and save result

        setattr(journal, 'present_day_%d' % current_date.day, present)
        journal.save()

        # return success status
        return JsonResponse({'status': 'success'})


class JournalSpecificStudentView(generic.TemplateView):
    template_name = 'cabinet_/journal/journal_specific_student.html'

    def get_student(self, request, jid):
        return render(self, request, jid)


class JournalUpdateView(generic.TemplateView):
    template_name = 'cabinet_/journal/journal_update.html'
