import re
from django.core.exceptions import ValidationError


def validate_url(value):
    # Validates if string 'value' matches regular expression for URL
    if not re.match("((^http[s]?:\/{2})|(^www)|(^\/{1})|(^\#{1}))", value):
        raise ValidationError(
            '"{}" is not a valid link. URL must start with www or http:// or https:// for external links and with / for inside app links or # with page links'.format(
                value)
        )


def validate_color(value):
    # Validates if 'value' is a valid HEX color
    if not re.match("^\#([A-F]|[a-f]|[0-9]){6}$", value):
        raise ValidationError(
            '"{}" is not a valid hex color'.format(
                value)
        )
