from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.utils import avatar_upload_to


class User(AbstractUser):
    avatar = models.ImageField(_('avatar'), upload_to=avatar_upload_to, blank=True)
    about = models.TextField(_('about'), blank=True)

    REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS
