import os

from rest_framework.exceptions import ValidationError

ALLOWED_EXTENSIONS = ['.jpg', '.png', '.jpeg']

def validate_file_size(value):
    if value.size > 20000000:
        raise ValidationError('max file size: 20Mb')


def validate_extension(value):
    ext = os.path.splitext(value.name)[1]
    if not ext.lower() in ALLOWED_EXTENSIONS:
        raise ValidationError(f'not allowed file ext, allowed: {ALLOWED_EXTENSIONS}')

