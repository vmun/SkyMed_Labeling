import os
from datetime import date
from SkyMed_Labeling import settings


def avatar_image_path(instance, filename):
    return f'profiles/avatars/{date.today()}/{filename}'


def task_document_path(instance, filename):
    return f'markup/images/{instance.imagePack.id}/{filename}'


def task_delete_path(document):
    print(document.file)
    file_path = os.path.join(settings.MEDIA_ROOT, document.file.name)
    print(file_path)
    if os.path.isfile(file_path):
        os.remove(file_path)
