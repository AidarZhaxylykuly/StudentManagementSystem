from .tasks import send_grade_notification

def update_grade(student, course, new_grade):
    send_grade_notification.delay(student.email, new_grade)