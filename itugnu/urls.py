# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>
# Author: Ahmed Ihsan Erdem <ihsan@itugnu.org>

from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import logout, password_reset, password_reset_confirm, password_reset_complete
from django.conf.urls.static import static
from django.urls import path, include
from web import views


urlpatterns = [
    path('contact/', views.contact, name='ajax-contact'),
    path('lecture/register/', views.lectures_register, name='lecture-register'),
    path('logout/', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('i18n/', include('django.conf.urls.i18n')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('registration/', views.registration, name='registration'),
    # Login
    path('login/reset/done/', views.password_reset_done, name='password-reset-done'),
    path('login/reset/complete/', password_reset_complete,
         {'template_name': 'auth/password-reset-complete.html'},
         name='password_reset_complete'),
    path('login/reset/<uidb64>/<token>/',
         password_reset_confirm,
         {'template_name': 'auth/password-reset-confirm.html'},
         name='password_reset_confirm'),
    path('login/reset/', password_reset,
         {
            'template_name': 'auth/password-reset.html',
            'email_template_name': 'auth/password-reset-email.html',
            'post_reset_redirect': 'password-reset-done',
         }, name='password-reset'),
    path('login/', views.login_view, name='login'),
    # Lectures
    path('lectures/', views.lectures_list, name='lectures-index'),
    path('faq/', views.faq, name='faq'),
    path('oyz/', views.oyz, name='oyz'),
    path('', views.index, name='index'),
    path('blog/', include('pinax.blog.urls', namespace='pinax_blog')),
) + urlpatterns

if settings.DEBUG and settings.DEBUG_TOOLBAR:
    import debug_toolbar  # pragma: no cover
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns  # pragma: no cover
