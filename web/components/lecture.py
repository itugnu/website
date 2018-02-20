# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

# from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from lecture.models import Lecture
from lecture.filters import LectureFilter


def lectures_list(request):
    lectures = LectureFilter(request.GET, queryset=Lecture.objects.all())
    data = {'lectures': lectures}
    return render(request, "lectures/index.html", data)
