from dataclasses import field
from rest_framework import serializers

from appointments.models import Appointment
from prescriptions.models import Prescription


# This Is For Admin Only
class PrescriptionSerializerForAdmin(serializers.ModelSerializer):

    class Meta:
        model = Prescription
        fields = [
            "uuid",
            "appointment",
            "doctor",
            "patient",
            "diagnosis",
            "notes",
            "follow_up_date",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        appointment = validated_data.get("appointment")
        doctor = validated_data.get("doctor")
        patient = validated_data.get("patient")

        if appointment.doctor != doctor:
            raise serializers.ValidationError(
                {"detail": "Selected Doctor And Appointment's Doctor Not Matched!"}
            )

        if appointment.patient != patient:
            raise serializers.ValidationError(
                {
                    "detail": "Selected Patient and Appointment's Patient are Not Matched!"
                }
            )

        if appointment.status != Appointment.Status.CONFIRMED:
            raise serializers.ValidationError(
                {"detail": "This Appointment is Not Confirmed"}
            )

        return super().create(validated_data)


class PrescriptionUpdateSerializerForAdmin(serializers.ModelSerializer):

    class Meta:
        model = Prescription
        fields = [
            "diagnosis",
            "notes",
            "follow_up_date"
        ]

    def update(self, instance, validated_data):
      if instance.appointment.status == Appointment.Status.COMPLETED:
        raise serializers.ValidationError({
					"detail": "You Can't Update The Completed Appointment's Prescriotion"
				})

      return super().update(instance=instance, validated_data=validated_data)


# TODO: Doctor And Patient AUTO SELECT WHEN CREATE