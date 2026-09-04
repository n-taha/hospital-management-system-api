from django.contrib import admin
from tests.models import TestOrder, TestOrderItem, TestReport

admin.site.register(TestOrder)
admin.site.register(TestOrderItem)
admin.site.register(TestReport)
