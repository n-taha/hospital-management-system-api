from rest_framework import serializers
from appointments.models import Appointment
from payments.models import Invoice
from users.models import Doctor, Patient, User
from payments.models import InvoiceItem
from appointments.services import AppointmentService


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [  # noqa: RUF012
            "uuid",
            "patient",
            "doctor",
            "schelued_at",
            "duration_minutes",
            "status",
            "reason",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["uuid", "created_at", "updated_at"]

    def create(self, validated_data):
        appointment = Appointment.objects.create(**validated_data)
        if not Invoice.objects.filter(patient=appointment.patient, status=Invoice.Status.DRAFT).exists():
             Invoice.objects.create(appointment=appointment, patient=appointment.patient)

        return appointment

    def update(self, instance, validated_data):
        status = validated_data.get('status')
        patient = validated_data.get('patient')
        AppointmentService.update_appointment(instance, status, patient)
        return super().update(instance, validated_data)


class AppointmentSerializerForPatient(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["doctor", "reason", "notes"]  # noqa: RUF012

    def create(self, validated_data):
        user = self.context["request"].user
        patient = Patient.objects.get(user=user)
        appointment = Appointment.objects.create(patient=patient, **validated_data)
        if not Invoice.objects.filter(patient=patient, status=Invoice.Status.DRAFT).exists():
            Invoice.objects.create(appointment=appointment, patient=patient)
        return appointment


class AppointmentSerializerForDoctor(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [  # noqa: RUF012
            "patient",
            "schelued_at",
            "duration_minutes",
            "status",
            "reason",
            "notes",
        ]

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user
        doctor = Doctor.objects.get(user=user)
        appointment = Appointment.objects.create(doctor=doctor, **validated_data)
        if not Invoice.objects.filter(patient=appointment.patient, status=Invoice.Status.DRAFT).exists():
            Invoice.objects.create(appointment=appointment, patient=appointment.patient)
        return appointment

    def update(self, instance, validated_data):
        status = validated_data.get('status')
        patient = validated_data.get('patient')
        AppointmentService.update_appointment(instance, status, patient)
        return super().update(instance, validated_data)