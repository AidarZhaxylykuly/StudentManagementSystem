from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_grade_notification(student_email, grade):
    send_mail(
        'Your Grade Update',
        f'Your new grade is {grade}',
        'admin@school.com',
        [student_email],
        fail_silently=False,
    )