# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

from django import template
from django.core.cache import cache
from django.conf import settings
from libravatar import libravatar_url

register = template.Library()


@register.simple_tag(takes_context=True)
def avatar(context, email, size=128):
    """Get https libravatar url for email addresses.

    Usage: {% load libravatar %}{% avatar email 128 %}
    """
    if not email:
        return settings.LIBRAVATAR_DEFAULT.format(size=size)
    cache_key = "avatar:{email}:{size}".format(email=email, size=size)
    avatar_url = cache.get(cache_key)
    if not avatar_url:
        avatar_url = libravatar_url(
            email, https=True, default=settings.LIBRAVATAR_DEFAULT.format(size=size), size=size
        )
        cache.set(cache_key, avatar_url, 86400)
    return avatar_url
