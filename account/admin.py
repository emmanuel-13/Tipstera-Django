from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    model = User
    list_display = ['username', 'email', 'first_name', 'last_name', 'profile_type', 'is_staff']
    fieldsets = DefaultUserAdmin.fieldsets + (
        (None, {'fields': ('profile_type', 'phone_number', 'country',)}),
    )
    add_fieldsets = DefaultUserAdmin.add_fieldsets + (
        (None, {'fields': ('profile_type', 'phone_number', 'country',)}),
    )
