from django.contrib import admin
from ai.models import AIChatSession, AIMessage
# Register your models here.

admin.site.register(AIChatSession)
admin.site.register(AIMessage)
