# This file is part of ITUGnu Website, licensed under GNU GPLv3.
# Copyright: ITUGnu <info@itugnu.org>.
# Author: Emin Mastizada <emin@linux.com>

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from datetime import time
from lecture.models import Lecture, LectureSchedule, LectureApplication
from common.models import User


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
