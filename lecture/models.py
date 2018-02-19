# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

from django.utils.translation import ugettext_lazy as _
from django.db import models
from common.models import User


class Lecture(models.Model):
    name = models.CharField(_("Lecture Name"), max_length=255, blank=False, null=False)
    lecturer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='lectures', verbose_name=_("Lecturer")
    )
    classroom = models.CharField(_("Classroom"), max_length=255, blank=True, null=True)
    start_date = models.DateField(_("Start Date"), blank=True, null=True)
    end_date = models.DateField(_("End Date"), blank=True, null=True)
    is_registration_open = models.BooleanField(_("Open for Registration"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Lecture')
        verbose_name_plural = _('Lectures')
        ordering = ('created_at',)


class LectureSchedule(models.Model):
    DAYS_OF_WEEK = [
        (1, _("Monday")),
        (2, _("Tuesday")),
        (3, _("Wednesday")),
        (4, _("Thursday")),
        (5, _("Friday")),
        (6, _("Saturday")),
        (7, _("Sunday"))
    ]
    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE, related_name='schedules', verbose_name=_("Lecture")
    )
    start_time = models.TimeField(_("Start Time"))
    end_time = models.TimeField(_("End Time"))
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK, default=1)

    def __str__(self):
        return self.lecture.name

    class Meta:
        verbose_name = _('Lecture Schedule')
        verbose_name_plural = _('Lecture Schedules')
        ordering = ('day_of_week', 'start_time',)
