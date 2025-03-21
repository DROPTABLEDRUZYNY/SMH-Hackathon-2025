from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User

    ordering = ('email',)
    
    list_display = ('email','first_name', 'last_name')
    #list_filter = ()

admin.site.register(User, CustomUserAdmin)