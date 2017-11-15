from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms import ExamForm
from ..models.exam import Exam
from ..models.exam import ExamResult
from ..util import get_current_group


class ExamsListView(LoginRequiredMixin, generic.ListView):
    template_name = 'cabinet/exams/exams_list.html'
    model = Exam
    paginate_by = 10

    def get_queryset(self):
        queryset = Exam.objects.all()
        current_group = get_current_group(self.request)
        if current_group:
            queryset = queryset.filter(group_id=current_group)
        else:
            queryset = queryset
        return queryset


class ExamResultView(LoginRequiredMixin, generic.ListView):
    template_name = 'cabinet/exams/exam_results.html'
    model = ExamResult
    paginate_by = 10

    def get_queryset(self):
        return ExamResult.objects.all()


class ExamAddView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Exam
    template_name = 'cabinet/exams/exam_add_form.html'
    form_class = ExamForm
    success_url = reverse_lazy('exams_list')
    success_message = _('New exam of %(discipline_name)s had been added to DB!')


class ExamEditView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Exam
    template_name = 'cabinet/exams/exam_edit_form.html'
    form_class = ExamForm
    success_url = reverse_lazy('exams_list')
    success_message = _('%(discipline_name)s was updated!')


class ExamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Exam
    template_name = 'cabinet/exams/exam_delete_confirm.html'
    success_url = reverse_lazy('exams_list')
    success_message = _('%(discipline_name)s was deleted!')

    def get_success_url(self):
        messages.success(self.request, message=self.success_message)
        return self.success_url
