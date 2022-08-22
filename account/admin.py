from django.contrib import admin

from .models import Account

# Register your models here.
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined', 'is_active']
    exclude = ('password',)
