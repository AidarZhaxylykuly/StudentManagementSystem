from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Course, Enrollment
import logging
from django.utils.timezone import now

@receiver(post_save, sender=Course)
def clear_course_cache(sender, instance, **kwargs):
    cache.delete('all_courses')

@receiver(post_delete, sender=Course)
def clear_course_cache_on_delete(sender, instance, **kwargs):
    cache.delete('all_courses')


logger = logging.getLogger('myapp')

@receiver(post_save, sender=Enrollment)
def log_enrollment(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Student {instance.student.username} enrolled in course {instance.course.name} at {now()}")