# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

from django.test import TestCase
from common.models import User
from web.apps import WebConfig
from web.templatetags.webtools import dictindex
from web.templatetags.libravatar import avatar
import re


class WebAppTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(email="tester@itugnu.org", username="tester")

    def test_app_config(self):
        self.assertEqual(WebConfig.name, 'web')

    def test_webtools_dictindex(self):
        self.assertEqual(dictindex({'user': self.user}, 'user'), self.user)

    def test_libravatar(self):
        pattern = re.compile("https?://\S+?/\S+?\.(?:jpg|jpeg|gif|png)&s=64")
        self.assertIsNotNone(pattern.match(avatar(None, 'emin@linux.com', 64)))
        self.assertEqual(avatar(None, None, 64), "https://seccdn.libravatar.org/nobody/64.png")
