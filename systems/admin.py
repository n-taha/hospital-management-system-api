from django.contrib import admin
from systems.models import AuditLog, Notification

admin.site.register(AuditLog)
admin.site.register(Notification)
