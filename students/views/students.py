from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext as _
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms import StudentForm
from ..models.student import Student
from ..util import get_current_group


class StudentsListView(generic.ListView):
    paginate_by = 10
    template_name = 'cabinet/students/students_list.html'

    def get_context_data(self, **kwargs):
        # This method adds extra variables to template
        # get original context data from parent class
        context = super(StudentsListView, self).get_context_data(**kwargs)
        # tell template not to show logo on a page
        context['show_logo'] = False
        return context

    def get_queryset(self):
        # check if we need to show only one group of students
        current_group = get_current_group(self.request)
        if current_group:
            queryset = Student.objects.filter(student_group=current_group)
        else:
            # otherwise show all students
            queryset = Student.objects.order_by('last_name')
        order_by = self.request.GET.get('order_by', '')
        if order_by in ('last_name', 'first_name', 'ticket'):
            students = queryset.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                queryset = students.reverse()
        return queryset


class StudentAddView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    template_name = 'cabinet/students/student_add_form.html'
    form_class = StudentForm
    model = Student
    success_url = reverse_lazy('students_list')
    success_message = _('%(first_name)s %(last_name)s was successful added!')

    def form_valid(self, form):
        # This method is called when valid form data has been posted.
        # It should return an HttpResponse.
        # TODO notify student by email that he is added to group
        return super(StudentAddView, self).form_valid(form)


class StudentsEditView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    template_name = "cabinet/students/students_edit_form.html"
    model = Student
    form_class = StudentForm
    success_url = reverse_lazy('students_list')
    success_message = _('%(first_name)s %(last_name)s Successfull updated!')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super(StudentsEditView, self).form_valid(form)


class StudentsDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Student
    template_name = 'cabinet/students/students_confirm_delete.html'

    def get_success_url(self):
        return reverse('students_list',
                       messages.success(self.request,message=_('Student successful deleted')))
