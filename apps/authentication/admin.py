from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    # Define the fields to be used in displaying the User model.
    list_display = ('username', 'email', 'bio', 'profile_picture', 'is_staff')
    list_filter = ('is_staff', 'is_active')
    ordering = ('id',)
    search_fields = ('username', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'bio', 'profile_picture')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'bio', 'profile_picture', 'is_active', 'is_staff')}
        ),
    )
    # Hide the password field in the admin list display
    def password(self, obj):
        return "********"  # Mask the password

    password.short_description = 'Password'  # Optional: Set a short description for the password field

# Register the new CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
