from django.contrib import admin
from .models import Enterprise, Locker


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


@admin.register(Locker)
class LockerAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'enterprise',
        'card',
        'available',
        'created_at'
    )
    list_filter = ('available', 'enterprise', 'created_at')
    search_fields = ('number', 'enterprise__business_name', 'card__rfid')
    raw_id_fields = ('enterprise', 'card')
    list_editable = ('available',)
