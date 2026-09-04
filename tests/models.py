from django.db import models
import uuid
from users.models import Doctor, Patient
from appointments.models import Appointment
from payments.models import Invoice

class TestOrder(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        SAMPLE_PENDING = "sample_pending", "Sample Pending"
        SAMPLE_COLLECTED = "sample_collected", "Sample Collected"
        IN_LAB = "in_lab", "In Lab"
        PROCESSING = "processing", "Processing"
        REPORT_READY = "report_ready", "Report Ready"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    appointment = models.ForeignKey(Appointment, on_delete=models.PROTECT, related_name='tests')
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='tests')
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='tests')
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name='tests', null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField()
    total_ammount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status

class TestOrderItem(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SAMPLE_PENDING = "sample_pending", "Sample Pending"
        SAMPLE_COLLECTED = "sample_collected", "Sample Collected"
        PROCESSING = "processing", "Processing"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    ),
    test_order = models.ForeignKey(TestOrder, on_delete=models.PROTECT, related_name='orders')
    test_name = models.CharField(max_length=50)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    instruction = models.TextField()
    status = models.CharField(choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return self.test_name

class TestReport(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    test_order_item = models.ForeignKey(TestOrderItem, on_delete=models.PROTECT, related_name='reports')
    result = models.TextField()
    file = models.FileField(upload_to='test_reports/')
    remarks = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.result
