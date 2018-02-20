# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from web.components import *  # NOQA


def index(request):
    data = {}
    return render(request, 'index.html', data)
