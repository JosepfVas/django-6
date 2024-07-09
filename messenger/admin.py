from django.contrib import admin
from client.models import Client
from messenger.models import Message, Mailing, Attempt


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'body')
    list_filter = ('id', )


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_send_time', 'last_send_time', 'message', 'status')


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'response', 'attempt_time', 'created_at', 'client')
