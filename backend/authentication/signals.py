from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

@receiver(post_migrate)
def create_content_types(sender, **kwargs):
    # This ensures content types are created properly
    if sender.name == 'contenttypes':
        ContentType.objects.clear_cache()