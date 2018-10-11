# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.dispatch import Signal
from datetime import time
from lecture.models import Lecture, LectureSchedule, LectureApplication
from lecture.signals import lecture_pre_save
from lecture.apps import LectureConfig
from common.models import User
import os


test_gif = (
    b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
    b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
    b'\x02\x4c\x01\x00\x3b'
)


class LectureTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(email="tester@itugnu.org", username="tester")

    def test_lecture(self):
        lecture_name = "Test Lecture"
        lecture = Lecture.objects.create(
            name=lecture_name,
            description='Some lecture description.',
            lecturer=self.user,
            classroom='EEB0000',
            start_date=timezone.datetime(year=1994, month=4, day=8, hour=9),
            end_date=timezone.datetime(year=3001, month=5, day=28, hour=18),
            is_registration_open=True
        )
        lecture.poster = SimpleUploadedFile('test.gif', test_gif, content_type='image/gif')
        lecture.save()
        self.assertEqual(lecture.__str__(), lecture_name)
        self.assertEqual(lecture.weeks, 52549)
        self.assertIn('/media/lectures/{pk}/test'.format(pk=lecture.pk), lecture.poster.url)

    def test_app_config(self):
        self.assertEqual(LectureConfig.name, 'lecture')

    def test_deleting_old_poster(self):
        Signal().connect(receiver=lecture_pre_save, sender=Lecture)
        lecture = Lecture.objects.create(
            name="Test Lecture",
            lecturer=self.user,
            classroom='EEB0000',
            start_date=timezone.datetime(year=1994, month=4, day=8, hour=9),
            end_date=timezone.datetime(year=3001, month=5, day=28, hour=18),
            is_registration_open=True
        )
        lecture.poster = SimpleUploadedFile('test.gif', test_gif, content_type='image/gif')
        lecture.save()

        old_image = lecture.poster.file.name

        lecture.poster = SimpleUploadedFile('test2.gif', test_gif, content_type='image/gif')
        lecture.save()

        self.assertNotEqual(old_image, lecture.poster.file.name)
        self.assertIn('/media/lectures/{pk}/test2'.format(pk=lecture.pk), lecture.poster.url)
        self.assertFalse(os.path.exists(old_image))
        self.assertTrue(os.path.exists(lecture.poster.file.name))

        lecture.poster.delete()
        Signal().disconnect(receiver=lecture_pre_save, sender=Lecture)


class LectureScheduleTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.lecture_name = "Test Lecture"
        cls.user = User.objects.create(email="tester@itugnu.org", username="tester")
        cls.lecture = Lecture.objects.create(
            name=cls.lecture_name,
            lecturer=cls.user,
            classroom='EEB0000',
            start_date=timezone.datetime(year=1994, month=4, day=8, hour=9),
            end_date=timezone.datetime(year=3001, month=5, day=28, hour=18),
            is_registration_open=True
        )

    def test_lecture_schedule(self):
        schedule = LectureSchedule.objects.create(
            lecture=self.lecture,
            start_time=time(hour=15),
            end_time=time(hour=18),
            day_of_week=1
        )
        self.assertEqual(schedule.__str__(), self.lecture_name)
        self.assertEqual(schedule.length, 3)
        schedule.end_time = time(hour=18, minute=30)
        schedule.save()
        self.assertEqual(schedule.length, 3.5)


class LectureApplicationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.lecture_name = "Test Lecture"
        cls.user = User.objects.create(email="tester@itugnu.org", username="tester")
        cls.lecture = Lecture.objects.create(
            name=cls.lecture_name,
            lecturer=cls.user,
            classroom='EEB0000',
            start_date=timezone.datetime(year=1994, month=4, day=8, hour=9),
            end_date=timezone.datetime(year=3001, month=5, day=28, hour=18),
            is_registration_open=True
        )

    def test_lecture_application(self):
        application = LectureApplication.objects.create(
            lecture=self.lecture,
            user=self.user
        )
        self.assertFalse(application.is_approved)
        self.assertEqual(
            application.__str__(),
            "Application for {lecture} from {user}".format(user=self.user, lecture=self.lecture)
        )
