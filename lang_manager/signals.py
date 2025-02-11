from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.management import call_command
from .models import Language

@receiver(post_save, sender=Language)
def update_translation_files(sender, instance, **kwargs):
    if instance.is_active:
        call_command('makemessages', locale=[instance.code])
        call_command('compilemessages')
