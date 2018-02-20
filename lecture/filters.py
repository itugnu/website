# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

from django.utils.translation import ugettext_lazy as _
from django_filters import FilterSet, DateFilter
from django.forms.widgets import DateInput
from lecture.models import Lecture


class LectureFilter(FilterSet):
    start_date = DateFilter(
        'start_date', lookup_expr="gte", label=_("Start Date"),
        widget=DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Lecture
        fields = ['is_registration_open', 'start_date']
