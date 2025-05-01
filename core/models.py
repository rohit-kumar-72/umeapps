from django.db import models

# Create your models here.
class AnalysisLog(models.Model):
    query=models.TextField()
    tone=models.CharField(max_length=64)
    intent = models.CharField(max_length=128)
    suggestions = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.query}'
    