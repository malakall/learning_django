from django.core.exceptions import ValidationError

def validation(value):
    if value == "":
        raise ValidationError("а кто заполнять будет, васька?",  params={'value': value},)