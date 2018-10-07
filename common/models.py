# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from common.managers import UserManager


class User(AbstractUser):
    PhoneValidator = RegexValidator(
        regex=r'^\+?1?\d{7,16}$',
        message=_("Phone number must be entered in the format: '+9055555'. Up to 16 digits allowed.")
    )
    email = models.EmailField(
        _('Email'), unique=True, blank=False, null=False,
        error_messages={
            'unique': _("A user with that email address already exists."),
        },
    )
    phone = models.CharField(_("Phone Number"), validators=[PhoneValidator], null=True, blank=True, max_length=30)
    language = models.CharField(choices=settings.LANGUAGES, default='tr', max_length=10)
    is_student = models.BooleanField(_("Student"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def get_full_name(self):
        if self.first_name and self.last_name:
            return ' '.join([self.first_name, self.last_name])
        return '@' + self.username

    def __str__(self):
        return self.get_full_name()

    @property
    def is_moderator(self):
        if self.is_staff:
            return True
        if self.groups.filter(name='Moderators').exists():
            return True
        return False

    @classmethod
    def get_random_username(cls, email, counter=0):
        """Get random username using email field.
        :param email: First part of email
        :param counter: Recursion counter
        """
        if counter:
            username = email + str(counter)
        else:
            username = email
        if cls.objects.filter(username=username).exists():
            counter += 1
            return cls.get_random_username(email, counter)
        return username

    def save(self, *args, **kwargs):
        if not self.username and self.email:
            self.username = User.get_random_username(self.email.split('@')[0])
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ('created_at',)
        indexes = [models.Index(fields=['email'], name='email_idx')]
