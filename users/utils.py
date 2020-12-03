import uuid
from pathlib import Path
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_passwords(password, password_confirmed):
    if password != password_confirmed:
        raise ValidationError(detail={'password_confirmed': _("Passwords don't match.")})


def avatar_upload_to(instance, filename):
    name = uuid.uuid4()
    extensions = Path(filename).suffixes
    return f'users/avatars/{instance.username.lower()}-{name}{"".join(extensions)}'
