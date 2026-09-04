from django.db import models
import uuid
from users.models import Doctor, Patient

# Create your models here.
class Appointment(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'Scheduled'
        CONFIRMED = 'confirmed', 'Confirmed'
        CHECKED_IN = 'checked_in', 'Checked IN'
        IN_PROGRESS = 'in_progress', 'IN Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELED = 'canceled', 'Canceled'
        NO_SHOW = 'no_show', 'NO Show'
        RESCHEDULED = 'rescheduled', 'Rescheduled'
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='patients')
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='doctors')
    schelued_at = models.DateTimeField(null=True, blank=True)
    duration_minutes =  models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    reason = models.CharField(max_length=500)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status

