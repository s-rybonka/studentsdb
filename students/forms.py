from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.urlresolvers import reverse
from students.models import Student
import magic
from django.core.exceptions import ValidationError
from studentsdb.settings import CONTENT_TYPES, MAX_UPLOAD_SIZE
from django.core.mail import send_mail
from studentsdb.local_settings import MANAGERS
from .widgets import ImageWidget
from django.utils.translation import ugettext as _
from .models.group import Group

from .models.exam import Exam
from .models.journal import Journal


# Students FORM

class ContactForm(forms.Form):
    from_email = forms.EmailField(label=_('Email'))
    subject = forms.CharField(label=_('Subject'), max_length=128)
    message = forms.CharField(label=_('Message'), max_length=2500, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        # call origin initializator
        super(ContactForm, self).__init__(*args, **kwargs)

        # this helper object allow us to customize form
        self.helper = FormHelper()

        # form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('contact-admin')

        # twiter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # form button
        self.helper.add_input(Submit('send_button', 'Send'))

    def send_email(self):
        email_from = self.cleaned_data.get('from_email')
        subject = self.cleaned_data.get('subject')
        message = self.cleaned_data.get('message')

        return send_mail(subject, message, email_from, MANAGERS)


class StudentForm(forms.ModelForm):
    last_name = forms.CharField(validators=[])
    birthday = forms.DateField(input_formats=['%d-%m-%Y', '%Y-%m-%d'], widget=forms.DateInput(
        attrs={'class': 'dateinput', 'addon_after': '<i class="fa fa-calendar" aria-hidden="true"></i>'}))

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'middle_name', 'birthday', 'photo', 'ticket', 'notes', 'student_group',)
        widgets = {
            'photo': ImageWidget
        }

    def clean_photo(self):
        cleaned_data = super(StudentForm, self).clean()
        file = cleaned_data.get('photo')

        if file:
            file_type = magic.from_buffer(file.read(), mime=True).format().split('/')[1].upper()

            if not file_type in CONTENT_TYPES:

                self.add_error('photo', forms.ValidationError(_('Invalid format for images, recommended PNG')))


            elif file.size > MAX_UPLOAD_SIZE:

                raise ValidationError(_('Invalid size.'))
        return file

    def clean_first_name(self):
        name = self.cleaned_data.get('first_name')
        if len(name) < 3:
            self.add_error('first_name', ValidationError(_('Short name')))
        else:
            return name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name[0].isupper():
            return last_name
        else:
            self.add_error('last_name', ValidationError(_('First litter should be Capitalize')))

    def clean_student_group(self):
        # take group_id from students table

        groups = Group.objects.filter(leader=self.instance).first()

        # check if student leader anywhere
        if groups:
            if self.cleaned_data.get('student_group') != groups:
                raise ValidationError(_('Student are leader in other group'), code='invalid')

        return self.cleaned_data['student_group']


# Group FORM

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['title', 'leader', 'notes']

        # To do, add some validation here if need

    def clean_leader(self):

        # take group_id from students table

        student_instance = self.cleaned_data.get('leader')

        if student_instance:

            if student_instance.student_group_id == self.instance.id:
                return student_instance
            else:
                self.add_error('leader', ValidationError(_('This student from other group.')))


# Exam Form

class ExamForm(forms.ModelForm):
    date = forms.DateTimeField(required=True, widget=forms.DateInput(
        attrs={'class': 'dateinput', 'addon_after': '<i class="fa fa-calendar" aria-hidden="true"></i>'}))

    class Meta:
        model = Exam
        fields = ['discipline_name', 'date', 'teacher_name', 'group_id']


# Journal Form

from datetimewidget.widgets import DateTimeWidget


class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['student', 'date', 'status']
        widgets = {
            'date': DateTimeWidget(usel10n=True, bootstrap_version=3)
        }
