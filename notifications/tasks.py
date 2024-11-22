from celery import shared_task
from django.core.mail import send_mail
from .models import Student, Grade, Attendance

@shared_task
def send_attendance_reminder():
    students = Student.objects.all()
    for student in students:
        send_mail(
            subject="Daily Attendance Reminder",
            message="Please mark your attendance for today.",
            from_email="admin@example.com",
            recipient_list=[student.email],
        )
    return "Attendance reminders sent."

@shared_task
def notify_grade_update(student_id, course_id, grade):
    student = Student.objects.get(id=student_id)
    course_name = student.enrollments.get(course_id=course_id).course.name
    send_mail(
        subject="Grade Updated",
        message=f"Your grade for {course_name} has been updated to {grade}.",
        from_email="admin@example.com",
        recipient_list=[student.email],
    )
    return f"Grade notification sent to {student.email}."
