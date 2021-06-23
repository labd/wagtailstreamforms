from django.core.serializers.json import DjangoJSONEncoder
from django.db import models


class FormSubmissionSerializer(DjangoJSONEncoder):
    """Form submission serializer"""

    def default(self, o):
        if isinstance(o, models.Model):
            return str(o)
        return super().default(o)
