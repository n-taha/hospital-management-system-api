from dataclasses import field
from django.forms import ValidationError
from django.utils.autoreload import raise_last_exception
from rest_framework import serializers

import appointments
from appointments.models import Appointment
from prescriptions.models import Prescription
from users.models import Doctor


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

        read_only_fields = ["doctor", "patient"]

    def create(self, validated_data):
        appointment = validated_data.get("appointment")

        validated_data['doctor'] = appointment.doctor
        validated_data['patient'] = appointment.patient

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


class PrescriptionSerializerForDoctor(serializers.ModelSerializer):

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
        read_only_fields = ["doctor", "patient"]


    def __init__(self,*args, **kwargs):

        super().__init__(*args, **kwargs)

        request = self.context.get('request')
        if request:
            doctor = Doctor.objects.filter(user=request.user).first()
            if doctor:
                self.fields["appointment"].queryset = Appointment.objects.filter(doctor=doctor, status=Appointment.Status.CONFIRMED)

    def validate(self, attrs):
        appointment = attrs.get('appointment')

        if appointment.status != Appointment.Status.CONFIRMED:
            raise ValidationError({
                "detail": "This Appointment is Not Confirm"
            })

        return attrs

    def update(self, instance, validated_data):

        appointment = validated_data.get('appointment', instance.appointment)

        if appointment != instance.appointment:
            raise serializers.ValidationError({
                "detail": "You can't update the appointment"
            })

        if instance.appointment.status == Appointment.Status.COMPLETED:
            raise ValidationError({
                "detail" : "You Can't Update Completed Appointment's Prescription"
            })


        super().update(instance=instance, validated_data=validated_data)


    def create(self, validated_data):
        appointment = validated_data.get('appointment')

        validated_data['doctor'] = appointment.doctor
        validated_data['patient'] = appointment.patient

        return super().create(validated_data)


class PrescriptionSerailzerForPatient(serializers.ModelSerializer):

    class Meta:
        model = Prescription
        fields = '__all__'
        read_only_fields = [
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
