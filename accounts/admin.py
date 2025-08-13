from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, UserLodge, Brother


class UserLodgeInline(admin.TabularInline):
    model = UserLodge
    extra = 1


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups',)
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')
    ordering = ('username',)
    inlines = [UserLodgeInline]

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Informações pessoais'), {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        (_('Permissões'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Datas importantes'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'phone_number',),
        }),
    )


@admin.register(Brother)
class BrotherAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_lodges', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    list_filter = ('userlodge__lodge',)
    readonly_fields = ('get_full_name', 'get_lodges', 'email', 'phone_number', 'username', 'first_name', 'last_name')
    
    list_display_links = None    
    actions = None

    def has_module_permission(self, request):
        return request.user.is_authenticated

    def has_view_permission(self, request, obj=None):
        return request.user.is_authenticated

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_superuser=False)
    
    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username
    get_full_name.short_description = _('Nome')
    get_full_name.admin_order_field = 'first_name'
    
    def get_lodges(self, obj):
        lodges = obj.userlodge_set.all().values_list('lodge__name', flat=True)
        return ', '.join(lodges) if lodges else '-'
    get_lodges.short_description = _('Lojas')
