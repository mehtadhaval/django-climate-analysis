from django.core.exceptions import ValidationError
from django.db.models.fields import FloatField


class CustomFloatField(FloatField):
    """
    If invalid data is given ignores it instead of raising exception
    """
    def to_python(self, value):
        if value is None:
            return value
        try:
            return super(CustomFloatField, self).to_python(value)
        except ValidationError:
            return None

    def get_prep_value(self, value):
        if value is None:
            return value
        try:
            return super(CustomFloatField, self).get_prep_value(value)
        except (TypeError, ValueError):
            return None
