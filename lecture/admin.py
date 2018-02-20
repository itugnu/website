# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from reversion.admin import VersionAdmin
from lecture.models import Lecture, LectureSchedule, LectureApplication


class InlineScheduleAdmin(admin.TabularInline):
    model = LectureSchedule
    fieldsets = (
        ('', {
            'fields': ('start_time', 'end_time', 'day_of_week',)
        }),
    )


@admin.register(Lecture)
class LectureAdmin(VersionAdmin):
    list_display = (
        'pk', 'name', 'lecturer', 'classroom', 'start_date', 'end_date', 'is_registration_open', 'created_at',
    )
    list_filter = (
        'classroom', ('lecturer', admin.RelatedOnlyFieldListFilter),
        'is_registration_open', 'start_date', 'created_at',
    )
    fieldsets = (
        (_('Lecture Information'), {
            'fields': ('name', 'description', 'poster', 'lecturer', ('classroom', 'is_registration_open'),)
        }),
        (_('Dates'), {
            'fields': (('start_date', 'end_date'),)
        }),
        (_('Stamps'), {
            'fields': (('created_at', 'updated_at'),)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('name', 'classroom', 'lecturer')
    inlines = [
        InlineScheduleAdmin
    ]


@admin.register(LectureSchedule)
class LectureScheduleAdmin(VersionAdmin):
    list_display = ('pk', 'lecture', 'start_time', 'end_time', 'day_of_week',)
    list_filter = ()
    fieldsets = (
        ('', {'fields': ('lecture', ('start_time', 'end_time', 'day_of_week'),)}),
    )


@admin.register(LectureApplication)
class LectureApplicationAdmin(VersionAdmin):
    list_display = ('pk', 'lecture', 'user', 'is_approved', 'created_at',)
    list_filter = (('lecture', admin.RelatedOnlyFieldListFilter), 'is_approved',)
    fieldsets = (
        (_('Application'), {
            'fields': (('lecture', 'user'), 'is_approved',)
        }),
        (_('Stamps'), {
            'fields': (('created_at',),)
        }),
    )
    readonly_fields = ('created_at',)
