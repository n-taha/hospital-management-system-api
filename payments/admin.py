from django.contrib import admin
from payments.models import Invoice, InvoiceItem, ManualPayment


admin.site.register(Invoice)
admin.site.register(ManualPayment)
admin.site.register(InvoiceItem)
