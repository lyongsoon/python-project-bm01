from django.contrib import admin
from .models import Client, Order, OrderItem


@admin.register(Client, Order, OrderItem)
class ClientAdmin(admin.ModelAdmin):
    pass
