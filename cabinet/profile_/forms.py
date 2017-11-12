from django import forms
from timezone_field.forms import TimeZoneFormField

from studentsdb.settings import LANGUAGES


class SessionSettingsForm(forms.Form):
    timezone = TimeZoneFormField()
    language = forms.ChoiceField(choices=LANGUAGES)

