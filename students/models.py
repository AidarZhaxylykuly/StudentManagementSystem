from django.db import models
from courses.models import Course
from django.utils import timezone
from rest_framework import generics


class Student(models.Model):
    name = models.CharField(max_length=255, default='Aidar')
    email = models.EmailField(unique=True)
    dob = models.DateField(default=timezone.now)
    registration_date = models.DateTimeField(default=timezone.now)
    courses = models.ManyToManyField(Course, through='Enrollment', related_name='students')

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.name} enrolled in {self.course.name}"
