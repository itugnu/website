# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>
# Author: Ahmed Ihsan Erdem <ihsan@itugnu.org>

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from datetime import date
from lecture.models import Lecture
from common.forms import RegistrationForm, LoginForm
from common.models import User
from web.forms import ContactForm
from pinax.blog.models import Post
from web.components import *  # NOQA


def get_user(email):
    try:
        return User.objects.get(email=email.lower()).username
    except User.DoesNotExist:
        return None


def index(request):
    lectures = Lecture.objects.filter(start_date__gte=date.today())[:6]
    post = Post.objects.all()[0]
    data = {'lectures': lectures, 'post' : post,}
    return render(request, 'index.html', data)


def registration(request):
    if request.method == 'POST':
        next_url = request.POST.get('next', 'index')
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            login(request, user)
            return redirect(next_url)
        return render(request, 'auth/registration.html', {'form': form})
    form = RegistrationForm()
    return render(request, 'auth/registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        next_url = request.POST.get('next', 'index')
        form = LoginForm(request.POST)
        if form.is_valid():
            username = get_user(form.cleaned_data.get('email'))
            if not username:
                return render(request, 'auth/login.html', {'form': form, 'error': _("User not found")})
            _user = authenticate(username=username, password=form.cleaned_data.get('password'))
            if _user is not None:
                if _user.is_active:
                    login(request, _user)
                    return redirect(next_url)
                return render(request, 'auth/login.html', {'form': form, 'error': _("Account Disabled")})
            return render(request, 'auth/login.html', {'form': form, 'error': _("Invalid login credentials")})
        return render(request, 'auth/login.html', {'form': form})  # form errors
    form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})


def password_reset_done(request):
    """Page after password reset."""
    return render(request, 'auth/reset-done.html', {})


def faq(request):
    return render(request, 'faq.html')


def oyz(request):
    return render(request, 'oyz.html')


def contact(request):
    if request.method == 'GET':
        return JsonResponse({"message": _("Method not allowed")}, status=405)
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
