# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

from django.utils.translation import ugettext_lazy as _
from django.db import models
from datetime import timedelta
from common.models import User
from typing import Union
from os import path as ospath
import logging


logger = logging.getLogger(__name__)


def poster_upload_path(instance, filename):
    logger.debug("Uploading file {name} as {lecture} lecture poster".format(
        name=filename, lecture=instance.name
    ))
    return ospath.join('lectures', str(instance.pk), filename)


class Lecture(models.Model):
    name = models.CharField(_("Lecture Name"), max_length=255, blank=False, null=False)
    description = models.TextField(_("Description"), blank=True, null=True)
    poster = models.ImageField(_("Poster"), upload_to=poster_upload_path, blank=True, null=True)
    lecturer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='lectures', verbose_name=_("Lecturer")
    )
    classroom = models.CharField(_("Classroom"), max_length=255, blank=True, null=True)
    start_date = models.DateField(_("Start Date"), blank=True, null=True)
    end_date = models.DateField(_("End Date"), blank=True, null=True)
    is_registration_open = models.BooleanField(_("Open for Registration"), default=False)
    external_registration_url = models.URLField(_("External Registration URL"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def weeks(self) -> int:
        return int((self.end_date - self.start_date).days / 7)

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

    @property
    def length(self) -> Union[int, float]:
        diff = (
                       timedelta(hours=self.end_time.hour, minutes=self.end_time.minute) -
                       timedelta(hours=self.start_time.hour, minutes=self.start_time.minute)
               ).seconds / 60 / 60
        if diff % 1 == 0.0:
            return int(diff)
        return round(diff, 1)

    def __str__(self):
        return self.lecture.name

    class Meta:
        verbose_name = _('Lecture Schedule')
        verbose_name_plural = _('Lecture Schedules')
        ordering = ('day_of_week', 'start_time',)


class LectureApplication(models.Model):
    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE, related_name='applicants', verbose_name=_("Lecture")
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='applications', verbose_name=_("User")
    )
    is_approved = models.BooleanField(_("Approved"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Application for {lecture} from {user}".format(
            lecture=self.lecture.name, user=self.user
        )

    class Meta:
        verbose_name = _('Lecture Application')
        verbose_name_plural = _('Lecture Applications')
        ordering = ('lecture', 'created_at',)
