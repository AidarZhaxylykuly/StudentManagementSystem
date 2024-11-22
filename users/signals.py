import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.timezone import now

logger = logging.getLogger('myapp')

@receiver(post_save, sender=User)
def user_registered(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New user registered: {instance.username} at {now()}. Email: {instance.email}")

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    logger.info(f"User logged in: {user.username} at {now()}")

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    logger.info(f"User logged out: {user.username} at {now()}")
