from modeltranslation.translator import translator, TranslationOptions
from .models.student import Student


class StudentTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name',)


translator.register(Student, StudentTranslationOptions)
