from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Attendance
import logging
from django.utils.timezone import now

logger = logging.getLogger('myapp')

@receiver(post_save, sender=Attendance)
def log_attendance(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Attendance marked for student {instance.student.username} in course {instance.course.name} at {now()}")