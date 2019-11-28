import os
from datetime import date
from SkyMed_Labeling import settings

ALLOWED_EXTENSIONS = ['.jpg', '.png', ]


def task_document_path(instance, filename):
    return f'markup/images/{date.today()}/{filename}'


def task_delete_path(document):
    print(document.document)
    file_path = os.path.join(settings.MEDIA_ROOT, document.document.name)
    print(file_path)
    if os.path.isfile(file_path):
        os.remove(file_path)
