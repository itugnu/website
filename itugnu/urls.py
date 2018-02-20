# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from web import views


urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG and settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
