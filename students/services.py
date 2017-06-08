from PIL import Image
from django.core.files.storage import FileSystemStorage
from django.utils.translation import ugettext as _

# Unnecessary code, only fo e.q.
def check_image_extensions(img_file, errors):
    file_input = str(img_file)
    available_formats = ['.jpg', '.png']
    if not file_input[-4:] in available_formats:
        errors['photo'] = _('Invalid format for files')


def check_extensions_pil(file_name, errors):
    content_type = Image.open(file_name, mode='r')
    fl = FileSystemStorage()
    im = fl.open(file_name)
    ins = Image.open(im)
    if str(ins) in ['PNG']:
        print('PNG')
