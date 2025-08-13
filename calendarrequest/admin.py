from django.contrib import admin

from .models import StoreRequest, CancelEventRequest, UserRequest


@admin.register(StoreRequest)
class StoreRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'number', 'user', 'approved')
    list_filter = ('approved', 'city',)
    search_fields = ('name', 'user__username', 'city', 'number')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if obj is None:
            if 'user' in form.base_fields:
                form.base_fields['user'].initial = request.user

        # Disable all fields if the request is approved
        if obj and obj.approved:
            for field_name in form.base_fields:
                form.base_fields[field_name].disabled = True
        else:
            if not request.user.is_superuser:
                if 'user' in form.base_fields:
                    form.base_fields['user'].disabled = True
                if 'approved' in form.base_fields:
                    form.base_fields['approved'].disabled = True
        
        return form

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.approved:
            return [f.name for f in self.model._meta.fields]
        return super().get_readonly_fields(request, obj)

    def has_change_permission(self, request, obj=None):
        if obj and obj.approved:
            return False
        if obj and not request.user.is_superuser and request.method == 'POST':
            if 'approved' in request.POST:
                pass
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.approved:
            return False
        return request.user.is_superuser

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        obj = self.get_object(request, object_id)
        if obj and obj.approved:
            extra_context['show_save'] = False
            extra_context['show_save_and_continue'] = False
            extra_context['show_save_and_add_another'] = False
            extra_context['show_delete'] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


@admin.register(CancelEventRequest)
class CancelEventRequestAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'reviewed')
    list_filter = ('reviewed',)
    search_fields = ('event__title', 'user__username')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if obj is None:
            if 'user' in form.base_fields:
                form.base_fields['user'].initial = request.user

        if not request.user.is_superuser:
            if 'user' in form.base_fields:
                form.base_fields['user'].disabled = True
            if 'reviewed' in form.base_fields:
                form.base_fields['reviewed'].disabled = True
        
        return form

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(UserRequest)
class UserRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'email', 'phone', 'lodge_number', 'approved')
    list_filter = ('approved',)
    search_fields = (
        'name',
        'surname',
        'email',
        'phone',
        'lodge_name',
        'lodge_number'
    )
    readonly_fields = (
        'name',
        'surname',
        'email',
        'phone',
        'lodge_name',
        'lodge_number',
        'message',
        'created_at',
        'updated_at'
    )

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.approved:
            return [f.name for f in self.model._meta.fields]
        return self.readonly_fields
