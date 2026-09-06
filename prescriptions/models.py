from django.db import models
import uuid
from appointments.models import Appointment
from users.models import Doctor, Patient
from medicines.models import Medicine


class Prescription(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    appointment = models.ForeignKey(Appointment, on_delete=models.PROTECT ,related_name="prescriptions")
    doctor = models.ForeignKey(Doctor,on_delete=models.PROTECT, related_name="prescriptions")
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="prescriptions")
    diagnosis = models.TextField()
    notes = models.TextField()
    follow_up_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT, related_name='items')
    dosages = models.CharField(max_length=100)
    frequency = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    instructions = models.TextField()


class MedicalRecord(models.Model):
    class RecordType(models.TextChoices):
        CONSULTATION = "consultation", "Consultation"
        DIAGNOSIS = "diagnosis", "Diagnosis"
        PRESCRIPTION = "prescription", "Prescription"
        LAB_RESULT = "lab_result", "Lab Result"
        RADIOLOGY = "radiology", "Radiology Report"
        PROCEDURE = "procedure", "Procedure"
        SURGERY = "surgery", "Surgery"
        VITAL_SIGNS = "vital_signs", "Vital Signs"
        ALLERGY = "allergy", "Allergy"
        IMMUNIZATION = "immunization", "Immunization"
        MEDICATION = "medication", "Medication Record"
        PROGRESS_NOTE = "progress_note", "Progress Note"
        DISCHARGE_SUMMARY = "discharge_summary", "Discharge Summary"
        REFERRAL = "referral", "Referral"
        EMERGENCY = "emergency", "Emergency Record"
        FOLLOW_UP = "follow_up", "Follow Up"
        MEDICAL_CERTIFICATE = "medical_certificate", "Medical Certificate"
        OTHER = "other", "Other"
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='records')
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='records')
    record_type = models.CharField(choices=RecordType.choices, default=RecordType.CONSULTATION)
    diagnosis = models.TextField()
    notes = models.TextField()
    file_url = models.FileField(upload_to='medical_records' ,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
