from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class APIUsageLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"API log for {self.user} at {self.timestamp}"


class PopularCourse(models.Model):
    course_id = models.PositiveIntegerField()
    views = models.PositiveIntegerField(default=0)