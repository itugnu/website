# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

from django.test import TestCase
from django.contrib.auth.models import Group
from common.apps import CommonConfig
from common.models import User
from common.forms import RegistrationForm


class UserManagerTestCase(TestCase):
    email = "tester@itugnu.org"
    username = "tester"

    def test_apps(self):
        self.assertEqual(CommonConfig.name, 'common')

    def test_create_user(self):
        user = User.objects.create_user(username=self.username, email=self.email, password="test")
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.username, self.username)
        self.assertTrue(user.has_usable_password())
        self.assertEqual(user.__str__(), '@' + self.username)
        user.first_name = "Tester"
        user.last_name = "Dummy"
        self.assertEqual(user.__str__(), "Tester Dummy")

    def test_empty_username(self):
        user = User.objects.create_user(email=self.email, username=None)
        self.assertTrue(bool(user.username))

    def test_empty_email(self):
        with self.assertRaisesMessage(ValueError, 'The given email must be set'):
            User.objects.create_user(username=self.username)

    def test_moderator(self):
        user = User.objects.create_user(username=self.username, email=self.email, password="test")
        self.assertFalse(user.is_moderator)
        # All staff users has moderator permissions
        user.is_staff = True
        self.assertTrue(user.is_moderator)
        # Check for Moderators group
        user.is_staff = False
        group = Group.objects.create(name="Moderators")
        group.user_set.add(user)
        self.assertTrue(user.is_moderator)

    def test_random_usernames(self):
        user = User.objects.create_user(username=None, email=self.email, password="test")
        self.assertEqual(user.username, "tester")
        user = User.objects.create_user(username=None, email=self.email + 'a', password="test")
        self.assertEqual(user.username, "tester1")
        user = User.objects.create_user(username=None, email=self.email + 'b', password="test")
        self.assertEqual(user.username, "tester2")

    def test_form_email(self):
        data = {'email': self.email, 'password': "test123"}
        form = RegistrationForm(data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertNotEqual(user.password, "test123")
        form = RegistrationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(list(form.errors.keys()), ['email'])
