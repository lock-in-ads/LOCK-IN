from django.contrib import admin
from .models import Enterprise, Card, Locker


# Register your models here.
@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'legal_name', 'cnpj', 'email', 'phone')
    search_fields = ('business_name', 'legal_name', 'cnpj')
    list_filter = ('created_at',)
    filter_horizontal = ('address',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('legal_name', 'business_name', 'cnpj')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'description')
        }),
        ('Addresses', {
            'fields': ('address',)
        }),
    )


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('rfid', 'enterpise_id', 'available', 'created_at')
    list_filter = ('available', 'enterpise_id', 'created_at')
    search_fields = ('rfid', 'enterpise_id__business_name')
    raw_id_fields = ('enterpise_id',)
    list_editable = ('available',)


@admin.register(Locker)
class LockerAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'enterpise_id',
        'card_id',
        'available',
        'created_at'
    )
    list_filter = ('available', 'enterpise_id', 'created_at')
    search_fields = ('number', 'enterpise_id__business_name', 'card_id__rfid')
    raw_id_fields = ('enterpise_id', 'card_id')
    list_editable = ('available',)
