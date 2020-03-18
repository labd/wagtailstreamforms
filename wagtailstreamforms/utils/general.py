from django.utils.text import slugify
from unidecode import unidecode


def get_slug_from_string(label):
    return str(slugify(str(unidecode(label))))
