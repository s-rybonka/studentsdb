from django import forms
from django.utils.safestring import mark_safe


class ImageWidget(forms.FileInput):
    def __init__(self, attrs=None):
        super(ImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []

        if value and hasattr(value, "url"):
            output.append(
                ('<br/><img class="img-thumbnail" src="%s" id="current_image" style="width:100px;"/>'
                 % (value.url)))
        output.append(super(ImageWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
