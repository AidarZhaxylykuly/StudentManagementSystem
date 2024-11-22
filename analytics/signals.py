from django.db.models.signals import post_save
from django.dispatch import receiver
from analytics.utils import send_to_google_analytics
from courses.models import Course

@receiver(post_save, sender=Course)
def log_course_interaction(sender, instance, **kwargs):
    send_to_google_analytics(user_id=instance.author.id, endpoint=f'/courses/{instance.id}')
