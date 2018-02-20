# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from web.forms import ContactForm
from web.components import *  # NOQA


def index(request):
    data = {}
    return render(request, 'index.html', data)


def contact(request):
    if request.method == 'GET':
        return JsonResponse({"response": _("Method not allowed")}, status=405)
    form = ContactForm(request.POST)
    if form.is_valid():
        send_mail(
            "ITUGnu Contact Form",
            str(form.cleaned_data['message']) +
            "\n\nFrom: " + str(form.cleaned_data['email']) + "\nPhone: " + str(form.cleaned_data['phone']),
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_CONTACT_EMAIL], fail_silently=False
        )
        return JsonResponse({}, status=200)
    errors = form.errors
    message = ""
    for error in errors:
        message += errors[error][0]
    return JsonResponse({"message": message}, status=400)
