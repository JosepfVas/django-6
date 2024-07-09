from django.contrib import admin
from client.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'comment')
    search_fields = ('full_name', 'email')
    list_filter = ('id', )

