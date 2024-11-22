from django.db import models
from django.conf import settings

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.CharField(max_length=255, default='Ayan Aksha')

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name="Студент"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name="Курс"
    )
    enrollment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата зачисления"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активное участие"
    )

    class Meta:
        unique_together = ('student', 'course')
        verbose_name = "Зачисление"
        verbose_name_plural = "Зачисления"

    def __str__(self):
        return f"{self.student.username} -> {self.course.name}"