from django.contrib import admin
from .models import Setup, Profession


@admin.register(Setup)
class SetupAdmin(admin.ModelAdmin):
    list_display = ('url', 'admin_email')
    fieldsets = (
        ('Configurações Básicas', {
            'fields': ('url', 'calendar_url')
        }),
        ('Email', {
            'fields': ('admin_email',)
        })
    )


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('name',)
    list_editable = ('is_active',)
    
    actions = ['activate_professions', 'deactivate_professions']
    
    def activate_professions(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} profissões foram ativadas.')
    activate_professions.short_description = "Ativar profissões selecionadas"
    
    def deactivate_professions(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} profissões foram desativadas.')
    deactivate_professions.short_description = "Desativar profissões selecionadas"