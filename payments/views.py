from django.views.generic import detail
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from payments.models import Invoice, InvoiceItem, ManualPayment
from users.models import Patient
from payments.serializers import (
    InvoiceItemSerializer,
    InvoiceSerializer,
    ManualPaymentSerializerForAdmin,
    ManualPaymentSerializerForPatient,
)
from payments.permissions import IsAdminOrCreateAndReadOnly, IsAdminOrReadOnly


class InvoiceViewSets(ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    lookup_field = "uuid"

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Invoice.objects.all()

        patient = Patient.objects.get(user=self.request.user)
        return Invoice.objects.filter(patient=patient)


class InvoiceItemViewSets(ModelViewSet):
    serializer_class = InvoiceItemSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "uuid"

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return InvoiceItem.objects.all()

        patient = Patient.objects.filter(user=self.request.user).first()
        if not patient:
            return InvoiceItem.objects.none()

        invoice = Invoice.object.filter(
            patient=patient, status=Invoice.Status.DRAFT
        ).first()
        if not invoice:
            return InvoiceItem.objects.none()

        return InvoiceItem.objects.filter(invoice=invoice)


class ManualPaymentviewSets(ModelViewSet):
    lookup_field = "uuid"
    permission_classes = [IsAuthenticated, IsAdminOrCreateAndReadOnly]

    def get_serializer_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return ManualPaymentSerializerForAdmin
        return ManualPaymentSerializerForPatient

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return ManualPayment.objects.all()
        patient = Patient.objects.filter(user=self.request.user).first()
        if not patient:
            return ManualPayment.objects.none()
        return ManualPayment.objects.filter(invoice__patient=patient)

    @action(
        methods=["patch"],
        detail=True,
        url_path="update_status",
        permission_classes=[IsAdminUser],
    )
    def update_status(self, request, pk=None):
        payment = self.get_object()

        new_status = request.data.get("status")

        if new_status not in ManualPayment.Status.values:
            return Response({"detail": "Invalid Status"}, status=HTTP_400_BAD_REQUEST)

        payment.status = new_status
        payment.save()

        return Response({"detail": "Status Updated"}, status=HTTP_200_OK)
