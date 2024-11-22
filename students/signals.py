from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Student

@receiver(post_save, sender=Student)
def clear_student_cache(sender, instance, **kwargs):
    cache.delete('all_students')

@receiver(post_delete, sender=Student)
def clear_student_cache_on_delete(sender, instance, **kwargs):
    cache.delete('all_students')