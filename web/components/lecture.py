# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from lecture.models import Lecture, LectureApplication
from lecture.filters import LectureFilter


def lectures_list(request):
    lectures = LectureFilter(request.GET, queryset=Lecture.objects.all())
    data = {'lectures': lectures}
    return render(request, "lectures/index.html", data)


def lectures_register(request):
    if request.method == 'GET':
        return JsonResponse({"message": _("Method not allowed")}, status=405)
    if not request.user.is_authenticated:
        return JsonResponse({"message": _("Please, login to register for lectures")}, status=403)
    lecture_pk = request.POST.get('lecture')
    try:
        lecture = Lecture.objects.get(pk=lecture_pk)
    except Lecture.DoesNotExist:
        return JsonResponse({"message": _("Lecture {pk} does not exist!").format(pk=lecture_pk)}, status=404)
    if not lecture.is_registration_open:
        return JsonResponse({"message": _("Lecture is not open for registration")}, status=403)
    if LectureApplication.objects.filter(lecture=lecture, user=request.user).exists():
        return JsonResponse({"message": _("You already registered for this lecture!")}, status=405)
    LectureApplication.objects.create(
        lecture=lecture,
        user=request.user
    )
    return JsonResponse({}, status=200)
