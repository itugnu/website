from django.test import TestCase
from django.test import Client
from django.shortcuts import reverse

from web import forms


class FormTestCase(TestCase):

    def setUp(self):
        self.correct_data = {

            'name': 'Rob Row',
            'email': 'robrow100@rrr.com',
            'phone': '76786136165',
            'message': "Hello, I'm Rob!"
        }

        self.incorrect_data = {
            'name': 'not_name',
            'email': 'not_email',
            'phone': '000000000',
            'message': ''
        }

    def test_is_valid(self):

        form = forms.ContactForm(data=self.correct_data)
        self.assertTrue(form.is_valid())

    def test_is_invalid(self):

        form = forms.ContactForm(data=self.incorrect_data)
        self.assertFalse(form.is_valid())


class ViewTestCase(TestCase):

    def setUp(self):
        self.username = 'Mon Lier'
        self.email = 'lier10@mon.com'
        self.password = 'imnotlier12345'

        self.client = Client()
        self.client.login(
            username=self.username,
            password=self.password

        )

    def test_view(self):
        urls = [
            'index',
            'logout',
            'registration',
            'password-reset-done',
            'password_reset_complete',
            'password-reset',
            'login',
            'lectures-index',
            'faq',
        ]

        for url in urls:
            response = self.client.get(reverse(url), follow=True)
            self.assertEqual(response.status_code, 200, msg="Can't get : %s" % url)
