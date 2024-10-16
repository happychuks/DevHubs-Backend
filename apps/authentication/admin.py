from django.contrib import admin
from .models import User, Profile

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')    
    search_fields = ('username', 'email')
    #ordering = ('id',)  
    
class ProfileAdmin(admin.ModelAdmin):
    list_editable = ['verified']
    list_display = ['full_name', 'user', 'verified']

admin.site.register(User,UserAdmin)
admin.site.register(Profile, ProfileAdmin)