# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>
# Author: Ahmed Ihsan Erdem <ihsan@itugnu.org>

from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from web import views


urlpatterns = [
    path('contact/', views.contact, name='ajax-contact'),
    path('i18n/', include('django.conf.urls.i18n')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('lectures/', views.lectures_list, name='lectures-index'),
    path('faq/', views.faq, name='faq'),
    path('', views.index, name='index'),
) + urlpatterns

if settings.DEBUG and settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
