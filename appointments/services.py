from django.db import transaction
from payments.models import Invoice, InvoiceItem
from appointments.models import Appointment

class AppointmentService:
    @classmethod
    @transaction.atomic
    def update_appointment(cls, instance, status, patient):
        invoice = Invoice.objects.get(patient=patient, status=Invoice.Status.DRAFT)
        if status == Appointment.Status.COMPLETED:
            InvoiceItem.objects.create(invoice=invoice, content_object=instance, fee=instance.doctor.consultation_fee)
