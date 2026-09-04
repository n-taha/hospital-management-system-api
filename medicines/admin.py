from django.contrib import admin
from medicines.models import Medicine, PharmacyStock
# Register your models here.

admin.site.register(Medicine)
admin.site.register(PharmacyStock)
