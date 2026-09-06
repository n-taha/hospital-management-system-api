from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from prescriptions.models import Prescription
from prescriptions.serializers import PrescriptionSerializerForAdmin

class PrescriptionViewSets(ModelViewSet):
  lookup_field = 'uuid'
  queryset = Prescription.objects.all()

  def get_serializer_class(self):
    if self.request.user.is_superuser or self.request.user.is_staff:
      return PrescriptionSerializerForAdmin