from .widgets import ColorWidget
from .validators import validate_color
from django.db import models


class ColorField(models.CharField):
    # Django model field for storing color data in database, with color validation
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 7
        kwargs['validators'] = [validate_color]
        super(ColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorWidget
        return super(ColorField, self).formfield(**kwargs)
