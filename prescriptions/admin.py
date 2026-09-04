from django.contrib import admin
from prescriptions.models import Prescription, PrescriptionItem, MedicalRecord
# Register your models here.

admin.site.register(Prescription)
admin.site.register(PrescriptionItem)
admin.site.register(MedicalRecord)