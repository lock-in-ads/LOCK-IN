from django.contrib import admin
from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('rfid', 'available', 'created_at')
    list_filter = ('available', 'created_at')
    search_fields = ('rfid', 'enterprise_id__business_name')
    list_editable = ('available',)
