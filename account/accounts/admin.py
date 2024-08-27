from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from . import models

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'is_active', 'is_staff', 'created_at', 'updated_at']
    search_fields = ['email',]
    list_filter = ['is_active', 'is_staff',]


    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', )}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',  'password1', 'password2'),
        }),
    )

    readonly_fields = ('last_login',)

admin.site.register(models.Role)
admin.site.register(models.RolePermissions)
admin.site.register(models.UserRole)

admin.site.register(models.User, UserAdmin)

admin.site.register(models.countries)
admin.site.register(models.states)
admin.site.register(models.cities)

# Custom Configuration
# Change the site header and title
admin.site.site_header = 'LetsGala'
admin.site.site_title = 'LetsGala'