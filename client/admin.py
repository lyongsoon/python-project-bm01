from django.contrib import admin
from .models import Client, Order


@admin.register(Client, Order)
class ClientAdmin(admin.ModelAdmin):
    pass
