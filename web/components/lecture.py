# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from lecture.models import Lecture, LectureApplication
from lecture.filters import LectureFilter


def lectures_list(request):
    lectures = LectureFilter(request.GET, queryset=Lecture.objects.all())
    data = {'lectures': lectures}
    return render(request, "lectures/index.html", data)


def lectures_register(request):
    if request.method == 'GET':
        return JsonResponse(
            {"message": _("Method not allowed"), "code": 'disabled_method'},
            status=405
        )
    if not request.user.is_authenticated:
        return JsonResponse(
            {"message": _("Please, login to register for lectures"), "code": 'login_required'},
            status=403
        )
    lecture_pk = request.POST.get('lecture')
    try:
        lecture = Lecture.objects.get(pk=lecture_pk)
    except Lecture.DoesNotExist:
        return JsonResponse(
            {"message": _("Lecture {pk} does not exist!").format(pk=lecture_pk), "code": 'not_found'},
            status=404
        )
    if not lecture.is_registration_open:
        return JsonResponse(
            {"message": _("Lecture is not open for registration"), "code": 'registration_closed'},
            status=403
        )
    if LectureApplication.objects.filter(lecture=lecture, user=request.user).exists():
        if lecture.external_registration_url:
            return JsonResponse(
                {
                    "message": _("You already registered for this lecture!"),
                    "code": 'duplicate_registration_with_external_form',
                    "url": lecture.external_registration_url
                },
                status=405
            )
        return JsonResponse(
            {"message": _("You already registered for this lecture!"), "code": 'duplicate_registration'},
            status=405
        )
    LectureApplication.objects.create(
        lecture=lecture,
        user=request.user
    )
    if lecture.external_registration_url:
        return JsonResponse(
            {
                "message": _("One more step, Complete this external form."),
                "code": 'external_form',
                "url": lecture.external_registration_url
            },
            status=200
        )
    return JsonResponse(
        {"message": _("Your application received."), "code": 'registration_success'},
        status=200
    )
