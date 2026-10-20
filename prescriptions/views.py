from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from prescriptions.models import Prescription, PrescriptionItem
from prescriptions.permissions import IsAdminOrDoctorOrReadOnly
from prescriptions.serializers import PrescriptionItemSerializerForAdmin, PrescriptionItemSerializerForDoctor, PrescriptionItemSerializerForPatient, PrescriptionSerailzerForPatient, PrescriptionSerializerForAdmin, PrescriptionSerializerForDoctor
from users.models import Doctor, Patient, User


class PrescriptionViewSets(ModelViewSet):
  lookup_field = 'uuid'
  permission_classes = [IsAuthenticated, IsAdminOrDoctorOrReadOnly]

  def get_serializer_class(self):
    if self.request.user.is_superuser or self.request.user.is_staff:
      return PrescriptionSerializerForAdmin
    elif self.request.user.role == User.Role.DOCTOR:
      return PrescriptionSerializerForDoctor
    return PrescriptionSerailzerForPatient

  def get_queryset(self):
    if self.request.user.is_superuser or self.request.user.is_staff:
      return Prescription.objects.all()

    elif self.request.user.role == User.Role.DOCTOR:
      doctor = Doctor.objects.filter(user=self.request.user).first()

      if doctor:
        return Prescription.objects.filter(doctor=doctor)
      return Prescription.objects.none()

    patient = Patient.objects.filter(user=self.request.user).first()

    if patient:
      return Prescription.objects.filter(patient=patient)
    return Prescription.objects.none()

class PrescriptionItemViewSets(ModelViewSet):

    permission_classes = [IsAuthenticated, IsAdminOrDoctorOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return PrescriptionItem.objects.all()

        if self.request.user.role == User.Role.DOCTOR:
            doctor = Doctor.objects.filter(user=self.request.user).first()
            if doctor:
                return PrescriptionItem.objects.filter(prescription__doctor=doctor)
            return PrescriptionItem.objects.none()

        patient = Patient.objects.filter(user=self.request.user).first()
        if patient:
            return PrescriptionItem.objects.filter(prescription__patient=patient)

        return PrescriptionItem.objects.none()

    def get_serializer_class(self):
       if self.request.user.is_superuser or self.request.user.is_staff:
           return PrescriptionItemSerializerForAdmin

       if self.request.user.role == User.Role.DOCTOR:
           return PrescriptionItemSerializerForDoctor

       return PrescriptionItemSerializerForPatient
