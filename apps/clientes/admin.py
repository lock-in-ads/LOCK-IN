from django.contrib import admin
from .models import Client


# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'phone',
        'access_level_display',
        'created_at'
    )
    search_fields = ('name', 'email', 'phone')
    list_filter = ('access_level', 'created_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'phone', 'access_level')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('address',),
        }),
    )
    filter_horizontal = ('address',)
    ordering = ('-created_at',)

    def access_level_display(self, obj):
        return obj.get_access_level_display()
    access_level_display.short_description = 'Access Level'
