# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

from django.test import TestCase
from common.models import User


class UserManagerTestCase(TestCase):
    email = "tester@itugnu.org"
    username = "tester"

    def test_create_user(self):
        user = User.objects.create_user(username=self.username, email=self.email, password="test")
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.username, self.username)
        self.assertTrue(user.has_usable_password())

    def test_empty_username(self):
        user = User.objects.create_user(email=self.email, username=None)
        self.assertTrue(bool(user.username))

    def test_empty_email(self):
        with self.assertRaisesMessage(ValueError, 'The given email must be set'):
            User.objects.create_user(username=self.username)
