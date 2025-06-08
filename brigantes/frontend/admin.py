from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUseradmin
from django.contrib import admin
from .models import Setting

# Register your models here.
@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):

    ordering = ['id', 'site_name', 'site_title']
    list_display = ['id', 'site_name', 'site_title']
    readonly_fields = ["id"]
