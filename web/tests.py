# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

from django.test import TestCase
from django.urls import reverse
from common.models import User
from web.apps import WebConfig
from web.templatetags.webtools import dictindex
from web.templatetags.libravatar import avatar
from web import views as webviews
import re


class WebAppTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_email = "tester@itugnu.org"
        cls.user_username = "tester"
        cls.user_password = "tester-password"
        cls.user = User.objects.create(email=cls.user_email, username=cls.user_username)
        cls.user.set_password(cls.user_password)
        cls.user.save()

    def test_app_config(self):
        self.assertEqual(WebConfig.name, 'web')

    def test_webtools_dictindex(self):
        self.assertEqual(dictindex({'user': self.user}, 'user'), self.user)

    def test_libravatar(self):
        pattern = re.compile("https?://\S+?/\S+?\.(?:jpg|jpeg|gif|png)&s=64")
        self.assertIsNotNone(pattern.match(avatar(None, 'emin@linux.com', 64)))
        self.assertEqual(avatar(None, None, 64), "https://seccdn.libravatar.org/nobody/64.png")

    def test_get_user(self):
        self.assertTrue(User.objects.filter(username=webviews.get_user('tester@itugnu.org')).exists())

    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_password_reset_done(self):
        response = self.client.get(reverse('password-reset-done'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/reset-done.html')

    def test_faq(self):
        response = self.client.get(reverse('faq'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faq.html')

    def test_oyz(self):
        response = self.client.get(reverse('oyz'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'oyz.html')

    def test_registration(self):
        response = self.client.get(reverse('registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/registration.html')
        self.assertTemplateUsed(response, 'django/forms/widgets/email.html')
        response = self.client.post(reverse('registration'), data={
            'next': 'faq',
            'first_name': 'Lev',
            'last_name': 'Tolstoy',
            'username': 'lev',
            'email': 'lev@tolstoy.rocks',
            'is_student': True,
            'password': 'roskolnikovsucks'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faq.html')
        self.assertTrue(User.objects.filter(username='lev').exists())
        # test with existing user
        response = self.client.post(reverse('registration'), data={
            'next': 'faq',
            'first_name': 'Lev',
            'last_name': 'Tolstoy',
            'username': 'lev',
            'email': 'lev@tolstoy.rocks',
            'is_student': True,
            'password': 'roskolnikovsucks'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/registration.html')

    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')
        # test login with email
        response = self.client.post(reverse('login'), data={
            'next': 'faq',
            'email': self.user_email,
            'password': self.user_password
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faq.html')
        # test login with invalid email
        response = self.client.post(reverse('login'), data={
            'next': 'faq',
            'email': self.user_username,
            'password': self.user_password
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')  # shows form errors for email
        # test invalid login credentials
        response = self.client.post(reverse('login'), data={
            'next': 'faq',
            'email': self.user_email,
            'password': 'somewrongpass'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')
        # test login with non-member email
        response = self.client.post(reverse('login'), data={
            'next': 'faq',
            'email': 'non@itugnu.org',
            'password': self.user_password
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')
        # test login with disable account
        user = User.objects.create(
            email='second@itugnu.org', username='second'
        )
        user.set_password('testpassword')
        user.is_active = False
        user.save()
        response = self.client.post(reverse('login'), data={
            'next': 'faq',
            'email': 'second@itugnu.org',
            'password': 'testpassword'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')

    def test_contact(self):
        response = self.client.get(reverse('ajax-contact'))
        self.assertEqual(response.status_code, 405)
        self.assertTrue('message' in response.json().keys())
        response = self.client.post(reverse('ajax-contact'), data={
            'name': 'Someone',
            'email': 'guest@itugnu.org',
            'message': 'Test message'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json().keys()), 0)
        # test wrong data
        response = self.client.post(reverse('ajax-contact'), data={
            'name': 'Someone',
            'email': 'not-an-email',
            'message': 'Test message'
        })
        self.assertEqual(response.status_code, 400)
        self.assertTrue('message' in response.json().keys())
