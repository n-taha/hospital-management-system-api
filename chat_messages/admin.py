from django.contrib import admin
from chat_messages.models import Message, Conversation, MessageAttachment

admin.site.register(Message)
admin.site.register(Conversation)
admin.site.register(MessageAttachment)
# Register your models here.
