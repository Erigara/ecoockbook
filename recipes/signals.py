from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from recipes.models import Chef


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_chef_receiver(sender, instance, created, **kwargs):
    if created:
        Chef.objects.create(user=instance)
