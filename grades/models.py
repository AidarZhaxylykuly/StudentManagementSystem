from django.db import models
from students.models import Student
from courses.models import Course
from django.utils import timezone

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=5)
    date = models.DateTimeField(default=timezone.now)
    teacher = models.CharField(max_length=255, default='Ayan Aksha')

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.name} - {self.course.name}: {self.grade}"