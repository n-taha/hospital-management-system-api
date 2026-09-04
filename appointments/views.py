from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from appointments.serializers import AppointmentSerializer, AppointmentSerializerForPatient, AppointmentSerializerForDoctor
from appointments.models import Appointment
from users.models import Doctor, Patient

class AppointmentViewSets(ModelViewSet):
    lookup_field = 'uuid'
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Appointment.objects.all()
        if self.request.user.role == 'doctor':
            doctor = self.request.user.doctors
            return Appointment.objects.filter(doctor=doctor)
        if self.request.user.role == 'patient':
            patient = self.request.user.patients
            return Appointment.objects.filter(patient=patient)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AppointmentSerializer
        if self.request.method in ['POST', 'PATCH', 'PUT', 'DELETE']:
            if self.request.user.is_superuser or self.request.user.is_staff:
                return AppointmentSerializer
            if self.request.user.role == 'doctor':
                return AppointmentSerializerForDoctor
            if self.request.user.role == 'patient':
                return AppointmentSerializerForPatient
            return AppointmentSerializerForPatient