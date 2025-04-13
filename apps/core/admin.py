from django.contrib import admin
from .models import Address


# Register your models here.
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'number', 'city', 'uf', 'cep')
    list_filter = ('uf', 'city')
    search_fields = ('street', 'city', 'cep', 'address_2')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('cep', 'street', 'number', 'city', 'uf')
        }),
        ('Additional Information', {
            'fields': ('address_2', 'reference_point'),
            'classes': ('collapse',)  # Makes this section collapsible
        }),
    )

    # If you want to customize how choices are displayed in the dropdown
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'uf':
            kwargs['choices'] = Address.UF_Choices.choices
        return super().formfield_for_choice_field(db_field, request, **kwargs)