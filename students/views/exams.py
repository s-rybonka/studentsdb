from django.views import generic
from ..models.exam import ExamResult
from ..models.exam import Exam
from ..forms import ExamForm
from  django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import reverse
from django.utils.translation import ugettext as _
from django.contrib import messages
from ..util import get_current_group


class ExamsListView(generic.ListView):
    template_name = 'cabinet_/exams/exams_list.html'
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


class ExamResultView(generic.ListView):
    template_name = 'cabinet_/exams/exam_results.html'
    model = ExamResult
    paginate_by = 10

    def get_queryset(self):
        return ExamResult.objects.all()


class ExamAddView(SuccessMessageMixin, generic.CreateView):
    model = Exam
    template_name = 'cabinet_/exams/exam_add_form.html'
    form_class = ExamForm
    success_url = '/exams'
    success_message = _('New exam of %(discipline_name)s had been addded to DB!')


class ExamEditView(SuccessMessageMixin, generic.UpdateView):
    model = Exam
    template_name = 'cabinet_/exams/exam_edit_form.html'
    form_class = ExamForm
    success_url = '/exams'
    success_message = _('%(discipline_name)s was updated!')


class ExamDeleteView(generic.DeleteView):
    model = Exam
    template_name = 'cabinet_/exams/exam_delete_confirm.html'

    def get_success_url(self):
        return reverse('exams_list', messages.add_message(self.request, messages.SUCCESS, _('Exam deleted successful!')))
