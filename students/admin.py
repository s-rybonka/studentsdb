from django.contrib import admin
from .models import Student, Group, Journal, Exam,LogEntry
from .models.exam import ExamResult
from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext as _


class StudentFormAdmin(ModelForm):
    def clean_student_group(self):
        """Check if student is leader in any group
        If yes, then ensure it's the same as selected group"""

        # get group where current student is leader
        groups = Group.objects.filter(leader=self.instance).first()

        # check if student leader anywhere
        if groups:
            if self.cleaned_data.get('student_group') != groups:
                raise ValidationError(_('Student are leader in other group'), code='invalid')

        return self.cleaned_data['student_group']


class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['student_group']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = ['last_name', 'first_name', 'middle_name', 'ticket', 'notes']
    form = StudentFormAdmin


class GroupFormAdmin(ModelForm):
    def clean_leader(self):
        # take group_id from students table

        student_instance = self.cleaned_data.get('leader')

        if student_instance.student_group_id == self.instance.id:

            return student_instance

        else:
            self.add_error('leader', ValidationError(_('This student from other group.')))


class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'leader']
    list_editable = ['leader']
    admin.site.empty_value_display = ['None']
    search_fields = ['title']
    form = GroupFormAdmin


class LogEntryAdmin(admin.ModelAdmin):
    ordering = ['-date']
    list_display = ['error_level','date','error_message']
    list_filter = ['error_level']
    search_fields = ['error_level','error_message']


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Journal)
admin.site.register(Exam)
admin.site.register(ExamResult)
admin.site.register(LogEntry,LogEntryAdmin)

