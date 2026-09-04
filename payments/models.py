from contextlib import nullcontext
import uuid

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

from appointments.models import Appointment
from users.models import Patient


class Invoice(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PENDING = "pending", "Pending"
        PARTIALLY_PAID = "partially_paid", "Partially Paid"
        PAID = "paid", "Paid"
        OVERDUE = "overdue", "Overdue"
        CANCELLED = (
            "cancelled",
            "Cancelled",
        )
        REFUNDED = "refunded", "Refunded"

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    patient = models.ForeignKey(
        Patient, on_delete=models.PROTECT, related_name="invoices"
    )
    appointment = models.ForeignKey(
        Appointment, on_delete=models.PROTECT, related_name="invoices"
    )
    doctor_fee = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True , default=0
    )
    test_fee = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, default=0
    )
    total_ammount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    paid_ammount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    due_ammount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    status = models.CharField(choices=Status.choices, default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User: {self.patient.user.first_name} with Total Ammount: {self.total_ammount} And Status: {self.status}'


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="items"
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        'content_type',
        'object_id'
    )
    fee = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)



class ManualPayment(models.Model):
    class PaymentMethod(models.TextChoices):
        BKASH = "bkash", "Bkash"
        NAGAD = "nagad", "Nagad"
        ROCKET = "rocket", "Rocket"
        DEVID_CARD = "devid_card", "Devid Card"
        CREDIT_CARD = "credit_card", "Credit Card"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        VERIFIED = "verified", "Verified"
        REJECTED = "rejected", "Rejected"
        CANCELLED = "cancelled", "Cancelled"

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    invoice = models.ForeignKey(
        Invoice, on_delete=models.PROTECT, related_name="manual_payments"
    )
    ammount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        choices=PaymentMethod.choices, default=PaymentMethod.BKASH
    )
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(
        max_length=30, choices=Status.choices, default=Status.PENDING
    )
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" User: {self.invoice.patient.user.first_name} With Ammount {self.ammount} is {self.status}"
