from django.db import models

# Create your models here.
class LLMRequest(models.Model):
    request = models.TextField()
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request {self.id} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
