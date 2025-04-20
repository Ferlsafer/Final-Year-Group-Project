# models.py
from django.db import models
from django.contrib.auth.models import User

class SymptomHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symptom = models.CharField(max_length=255)
    analysis_result = models.TextField()
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.symptom}"
