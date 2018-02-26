# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

from django.utils.translation import ugettext_lazy as _
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_slug
from common.models import User


class LoginForm(forms.Form):
    error_css_class = 'is-invalid'
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': _("Email *"),
            'class': 'form-control'
        })
    )

    password = forms.CharField(
        label=_("Password"),
        required=True,
        min_length=5,
        widget=forms.PasswordInput(attrs={
            'placeholder': _("Password *"),
            'class': 'form-control'
        })
    )


class RegistrationForm(forms.ModelForm, LoginForm):
    first_name = forms.CharField(
        label=_("First Name"),
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': _("First Name"),
            'class': 'form-control'
        })
    )

    last_name = forms.CharField(
        label=_("Last Name"),
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': _("Last Name"),
            'class': 'form-control'
        })
    )

    username = forms.CharField(
        label=_("Username"),
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': _("Username"),
            'class': 'form-control'
        }),
        validators=[validate_slug]
    )

    language = forms.ChoiceField(
        label=_("Language"),
        choices=settings.LANGUAGES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    phone = forms.CharField(
        label=_("Phone Number"),
        min_length=7,
        required=False,
        widget=forms.NumberInput(attrs={
            'placeholder': _("Phone Number"),
            'class': 'form-control phone-input'
        })
    )

    is_student = forms.ChoiceField(
        label=_("Student"),
        required=False,
        choices=((False, _("Not Student")), (True, _("Student"))),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'username', 'language', 'phone', 'is_student']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError(_("A user with that email address already exists."))
        return email
