from django.contrib import admin

from .models import User, LoginLog

admin.site.register(User)
@admin.register(LoginLog)
class LoginLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'ip_address', 'user_agent', 'country')
    list_filter = ('user', 'timestamp', 'ip_address', 'user_agent')
   
