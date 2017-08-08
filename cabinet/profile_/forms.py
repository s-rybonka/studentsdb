from django import forms
from timezone_field.forms import TimeZoneFormField
from django.utils import translation

from studentsdb.settings import LANGUAGES


class SessionSettingsForm(forms.Form):
    timezone = TimeZoneFormField()
    language = forms.ChoiceField(choices=LANGUAGES)

