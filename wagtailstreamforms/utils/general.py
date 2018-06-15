from unidecode import unidecode

from django.utils.text import slugify


def get_slug_from_string(label):
    return str(slugify(str(unidecode(label))))
