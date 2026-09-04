from django.db import models
import uuid
from users.models import Patient

class AIChatSession(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    patient = models.ForeignKey(Patient, related_name='sessions', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add= True)

class AIMessage(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    role = models.CharField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

