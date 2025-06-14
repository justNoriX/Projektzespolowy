from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class MaximumLengthValidator:
    def __init__(self, max_length=128):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(
                _(f"Hasło nie może mieć więcej niż {self.max_length} znaków."),
                code='password_too_long',
                params={'max_length': self.max_length},
            )
