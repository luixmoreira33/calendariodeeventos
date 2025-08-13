from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Event
from accounts.models import UserLodge, CustomUser


class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and start_time >= end_time:
            raise ValidationError(
                _('A data e hora de início do evento deve ser anterior à data e hora de término.')
            )

        return cleaned_data


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_display = ('title', 'lodge', 'start_time', 'end_time', 'address', 'user', 'is_cancelled')
    search_fields = ('title', 'description', 'address', 'user__username')
    list_filter = ('start_time', 'end_time', 'created_at', 'updated_at')
    readonly_fields = ('google_event_id',)

    def has_delete_permission(self, request, obj=None):
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        obj = self.get_object(request, object_id)
        
        if obj and obj.is_cancelled:
            extra_context['show_save'] = False
            extra_context['show_save_and_continue'] = False
            extra_context['show_save_and_add_another'] = False
            
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        form.base_fields['lodge'].required = True

        if obj and obj.is_cancelled:
            for field_name in form.base_fields:
                form.base_fields[field_name].disabled = True

        elif not request.user.is_superuser:
            form.base_fields['user'].disabled = True

        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "lodge" and not request.user.is_superuser:
            kwargs["queryset"] = UserLodge.objects.filter(
                user=request.user
            ).distinct()
        elif db_field.name == "user":
            kwargs["queryset"] = CustomUser.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
