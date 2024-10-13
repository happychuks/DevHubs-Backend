from django.contrib import admin
from .models import User, Profile

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'roles')
    ordering = ('username',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'user_email', 'user_roles', 'first_name', 'last_name', 'verified')
    search_fields = ('user__username', 'user__email', 'first_name', 'last_name')
    list_filter = ('verified',)
    ordering = ('user__username',)

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Username'

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'

    def user_roles(self, obj):
        return obj.user.roles
    user_roles.short_description = 'Roles'

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)