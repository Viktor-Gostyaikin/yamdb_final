from django.core.exceptions import ValidationError
from django.utils import timezone


def validator_year(val):
    current_year = timezone.now().year
    if val > current_year:
        raise ValidationError('Такой год еще не наступил')
