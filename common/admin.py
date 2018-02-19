# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from common.models import User
from django.contrib.auth.admin import UserAdmin as AbstractUserAdmin
from reversion.admin import VersionAdmin


@admin.register(User)
class UserAdmin(AbstractUserAdmin, VersionAdmin):
    """Custom user in Django Admin."""
    list_display = ('pk', '__str__', 'updated_at',)
    list_filter = ('created_at',)
    fieldsets = (
        (_('Account Info'), {
            'fields': ('first_name', 'last_name', 'username', 'email', 'phone',
                       'groups', 'is_staff', 'is_active',)
        }),
        (_('Password'), {
            'fields': ('password',)
        }),
        (_('Stamps'), {
            'fields': (('created_at', 'updated_at'),)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('username', 'email', 'phone', 'first_name', 'last_name',)
