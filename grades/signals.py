from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Grade
import logging
from django.utils.timezone import now

logger = logging.getLogger('myapp')

@receiver(post_save, sender=Grade)
def log_grade_update(sender, instance, created, **kwargs):
    logger.info(f"Grade for student {instance.student.username} updated to {instance.grade} in course {instance.course.name} at {now()}")