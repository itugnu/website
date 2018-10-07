# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from common.models import User
from common.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin as AbstractUserAdmin
from reversion.admin import VersionAdmin


@admin.register(User)
class UserAdmin(AbstractUserAdmin, VersionAdmin):
    """Custom user in Django Admin."""
    add_form = UserCreationForm
    list_display = ('pk', '__str__', 'updated_at',)
    list_filter = ('is_student', 'created_at',)
    fieldsets = (
        (_('Account Info'), {
            'fields': (('first_name', 'last_name'), 'username', 'email', ('phone', 'is_student'),
                       'groups', ('is_staff', 'is_superuser'), 'is_active',)
        }),
        (_('Password'), {
            'fields': ('password',)
        }),
        (_('Stamps'), {
            'fields': (('created_at', 'updated_at'), 'last_login',)
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'last_login')
    search_fields = ('username', 'email', 'phone', 'first_name', 'last_name',)
