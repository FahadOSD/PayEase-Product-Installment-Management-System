# accounts/admin.py

from django.contrib import admin
from .models import CustomUser, OTP
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'is_email_verified', 'is_staff']
    search_fields = ['email', 'username']
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OTP)