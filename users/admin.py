from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, Doctor, Patient
admin.site.register(Doctor)
admin.site.register(Patient)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('-date_joined',)

    readonly_fields = ('date_joined', 'last_login')
    actions = ('activate_users', 'deactivate_users')

    def activate_users(self, request, queryset):
        updated = queryset.update(is_active = True)
        self.message_user(request, f'Successfully {updated} user activated')
    activate_users.short_description = 'Active Selected User'

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Successfully {updated} users deactivated')
    deactivate_users.short_description = 'Deactive Selected Users'


    fieldsets = (
        ('Login Credential', {
            'fields':('email', 'password')
        }),
        ('Personal Info', {
            'fields':('first_name', 'last_name', 'phone_number', 'address')
        }),
        ('Permissions', {
            'fields':('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'role'),
            'classes':('collapse',)
        }),
        ('Important Dates', {
            'fields':('date_joined', 'last_login')
        }),
    )

    add_fieldsets = (
        ('Add User', {
            'classes':('wide',),
            'fields':('email', 'first_name', 'last_name', 'address', 'phone_number', 'password1', 'password2')
        }),
    )
