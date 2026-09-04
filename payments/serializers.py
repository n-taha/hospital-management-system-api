from rest_framework import serializers
from payments.models import Invoice, InvoiceItem, ManualPayment
from users.models import Patient, User

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['uuid', 'patient', 'appointment', 'doctor_fee', 'test_fee', 'total_ammount', 'paid_ammount', 'due_ammount', 'status', 'created_at', 'updated_at']
        read_only_fields = ['uuid', 'total_ammount', 'due_ammount', 'paid_ammount', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        if self.instance.status == Invoice.Status.PAID:
            raise serializers.ValidationError({'message': "Paid Invoice can't be updated"})
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.total_ammount = (instance.doctor_fee + instance.test_fee)
        instance.due_ammount =  instance.total_ammount - instance.paid_ammount
        instance.save()
        return instance

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['content_type', 'content_object', 'object_id', 'fee', 'description']


# this is for patient
class ManualPaymentSerializerForPatient(serializers.ModelSerializer):
    class Meta:
        model = ManualPayment
        fields = ['uuid', 'invoice', 'ammount', 'payment_method', 'transaction_id', 'status', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['uuid', 'status', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        request = self.context.get('request')
        if request:
            patient = Patient.objects.filter(user=request.user).first()
            if patient:
                self.fields["invoice"].queryset = Invoice.objects.filter(patient=patient, status=Invoice.Status.PENDING)

    def validate_invoice(self, invoice):
        request = self.context['request']
        patient = Patient.objects.filter(user=request.user).first()

        if patient:
            if invoice.patient != patient:
                raise serializers.ValidationError({
                    "detail":"You can't Select Another Person Invoice"
                })

            if invoice.status != Invoice.Status.PENDING:
                raise serializers.ValidationError({
                    "detail": "You Can Payment Only Pending Invoice"
                })
            return invoice

#this is for admin
class ManualPaymentSerializerForAdmin(serializers.ModelSerializer):
    class Meta:
        model = ManualPayment
        fields = ['uuid', 'invoice', 'ammount', 'payment_method', 'transaction_id', 'status', 'notes', 'created_at', 'updated_at']

