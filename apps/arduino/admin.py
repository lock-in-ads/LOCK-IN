from django.contrib import admin
from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('rfid', 'enterprise_id', 'available', 'created_at')
    list_filter = ('available', 'enterprise_id', 'created_at')
    search_fields = ('rfid', 'enterprise_id__business_name')
    raw_id_fields = ('enterprise_id',)
    list_editable = ('available',)
