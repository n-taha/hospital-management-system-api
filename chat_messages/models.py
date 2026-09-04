from django.db import models
from users.models import Patient, Doctor
from appointments.models import Appointment
import uuid
from users.models import User
from django.contrib.auth import get_user_model


User = get_user_model()

class Conversation(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='conversations')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='conversations')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='appointments')
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.is_active

class Message(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='messages')
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    sender_role = models.CharField()
    content = models.TextField()
    is_read = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.is_read


class MessageAttachment(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='message-file/')
    file_type = models.CharField(max_length=10)
    original_name = models.CharField(max_length=20)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file
