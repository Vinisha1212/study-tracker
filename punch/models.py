from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    total_minutes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.start_time.strftime('%d %b %Y, %I:%M %p')}"


class Break(models.Model):
    session = models.ForeignKey(StudySession, related_name='breaks', on_delete=models.CASCADE)
    break_start = models.DateTimeField(null=True, blank=True)
    break_end = models.DateTimeField(null=True, blank=True)
    break_minutes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Break for {self.session.user.username} ({self.break_minutes} mins)"
