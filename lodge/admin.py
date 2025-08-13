from django.contrib import admin
from django.db.models import Q

from .models import Lodge

@admin.register(Lodge)
class LodgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'number',)
    list_filter = ('city',)
    search_fields = ('name', 'user__username', 'city', 'number',)
    readonly_fields = ('created_at', 'updated_at',)
