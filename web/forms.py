# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

from django.utils.translation import ugettext_lazy as _
from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        label=_("Name"),
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': _("Full Name"),
            'required': 'required',
            'class': 'form-control',
        })
    )
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': _("Email Address"),
            'required': 'required',
            'class': 'form-control',
        })
    )
    phone = forms.CharField(
        label=_("Phone Number"),
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': _("Phone Number"),
            'class': 'form-control',
        })
    )
    message = forms.CharField(
        label=_("Message"),
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': _("Your Message"),
            'class': 'form-control',
        })
    )
